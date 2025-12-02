---
layout: post
title: "Laravel Sanctum vs Passport: Choosing the Right API Authentication"
date: 2025-12-02
tags: [laravel, api, authentication, security, sanctum, passport]
---

Choosing the wrong authentication package for your Laravel API can cost your team weeks of refactoring and introduce unnecessary complexity. With Laravel offering both Sanctum and Passport for API authentication, technical leads often struggle to determine which solution fits their specific requirements. Understanding the architectural differences between these packages is critical for building secure, maintainable APIs.

For tech leaders evaluating authentication strategies, the choice between Sanctum and Passport directly impacts development velocity, security posture, and long-term maintenance costs.

## Why This Matters for Your Team

API authentication decisions have cascading effects throughout your application architecture:

- **Development Speed**: Wrong choice means rebuilding authentication flows
- **Security Compliance**: Different packages offer different OAuth2 grant types
- **Scalability**: Token management strategies affect database performance
- **Third-Party Integration**: Some scenarios require full OAuth2 server capabilities
- **Mobile App Support**: Token refresh patterns vary significantly between packages

The investment in understanding these differences pays dividends in reduced technical debt and confident architectural decisions.

## Understanding Laravel Sanctum

Laravel Sanctum provides a lightweight authentication system for SPAs (Single Page Applications), mobile applications, and simple token-based APIs. It's designed for scenarios where you control both the frontend and backend.

### When to Choose Sanctum

```php
<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Illuminate\Validation\ValidationException;

class SanctumAuthController extends Controller
{
    /**
     * Issue API token for mobile application or SPA.
     * Sanctum excels when your frontend and API share the same domain.
     */
    public function login(Request $request)
    {
        $request->validate([
            'email' => 'required|email',
            'password' => 'required',
            'device_name' => 'required|string|max:255',
        ]);

        $user = User::where('email', $request->email)->first();

        if (!$user || !Hash::check($request->password, $user->password)) {
            throw ValidationException::withMessages([
                'email' => ['The provided credentials are incorrect.'],
            ]);
        }

        // Create token with specific abilities for fine-grained permissions
        $token = $user->createToken($request->device_name, [
            'read:profile',
            'update:profile',
            'read:orders',
        ]);

        return response()->json([
            'token' => $token->plainTextToken,
            'token_type' => 'Bearer',
            'user' => $user->only(['id', 'name', 'email']),
        ]);
    }

    /**
     * Revoke the current user's token.
     */
    public function logout(Request $request)
    {
        // Revoke only the current token
        $request->user()->currentAccessToken()->delete();

        return response()->json([
            'message' => 'Successfully logged out',
        ]);
    }

    /**
     * Revoke all tokens for enhanced security.
     */
    public function logoutAll(Request $request)
    {
        // Revoke all tokens for this user
        $request->user()->tokens()->delete();

        return response()->json([
            'message' => 'All sessions terminated',
        ]);
    }
}
```

### Sanctum SPA Authentication (Cookie-Based)

For SPAs served from the same domain, Sanctum provides seamless cookie-based authentication:

```php
<?php

// config/sanctum.php - Configure stateful domains for SPA authentication
return [
    'stateful' => explode(',', env('SANCTUM_STATEFUL_DOMAINS', sprintf(
        '%s%s',
        'localhost,localhost:3000,127.0.0.1,127.0.0.1:8000,::1',
        env('APP_URL') ? ','.parse_url(env('APP_URL'), PHP_URL_HOST) : ''
    ))),

    // Guard configuration
    'guard' => ['web'],

    // Token expiration (null = never expires)
    'expiration' => null,

    // Middleware for Sanctum routes
    'middleware' => [
        'verify_csrf_token' => \Illuminate\Foundation\Http\Middleware\VerifyCsrfToken::class,
        'encrypt_cookies' => \Illuminate\Cookie\Middleware\EncryptCookies::class,
    ],
];
```

```javascript
// Frontend SPA - Axios configuration for Sanctum cookie authentication
import axios from 'axios';

// Configure axios for CSRF protection
axios.defaults.withCredentials = true;

async function initializeSanctumAuth() {
    // First, get CSRF cookie
    await axios.get('/sanctum/csrf-cookie');
    
    // Now authenticate
    const response = await axios.post('/login', {
        email: 'user@example.com',
        password: 'password',
    });
    
    // Subsequent requests are automatically authenticated via cookies
    const user = await axios.get('/api/user');
    return user.data;
}
```

### Sanctum Token Abilities (Permissions)

```php
<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;

class OrderController extends Controller
{
    /**
     * Verify token has required ability before processing.
     */
    public function index(Request $request)
    {
        // Check if token has the required ability
        if (!$request->user()->tokenCan('read:orders')) {
            return response()->json([
                'error' => 'Insufficient permissions',
            ], 403);
        }

        $orders = $request->user()->orders()
            ->with('items')
            ->orderBy('created_at', 'desc')
            ->paginate(15);

        return response()->json($orders);
    }

    /**
     * Middleware-based ability checking.
     */
    public function store(Request $request)
    {
        // This can also be done via middleware:
        // Route::post('/orders', [OrderController::class, 'store'])
        //     ->middleware('ability:create:orders');

        $validated = $request->validate([
            'items' => 'required|array|min:1',
            'items.*.product_id' => 'required|exists:products,id',
            'items.*.quantity' => 'required|integer|min:1',
        ]);

        $order = $request->user()->orders()->create([
            'status' => 'pending',
            'total' => $this->calculateTotal($validated['items']),
        ]);

        return response()->json($order, 201);
    }

    private function calculateTotal(array $items): int
    {
        // Simplified for brevity - real implementation would fetch product prices
        return collect($items)->sum(fn($item) => 
            \App\Models\Product::find($item['product_id'])->price * $item['quantity']
        );
    }
}
```

## Understanding Laravel Passport

Laravel Passport provides a full OAuth2 server implementation. It's essential when you need to provide third-party access to your API or implement complex authentication flows.

### When to Choose Passport

```php
<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Laravel\Passport\TokenRepository;
use Laravel\Passport\RefreshTokenRepository;

class PassportAuthController extends Controller
{
    /**
     * Personal Access Token approach - For first-party applications.
     * For third-party apps, use authorization code with PKCE (shown below).
     */
    public function login(Request $request)
    {
        $credentials = $request->validate([
            'email' => 'required|email',
            'password' => 'required',
        ]);

        if (!Auth::attempt($credentials)) {
            return response()->json([
                'error' => 'Invalid credentials',
            ], 401);
        }

        $user = Auth::user();

        // Create OAuth2 token with scopes
        $token = $user->createToken('API Token', [
            'read-profile',
            'update-profile',
            'read-orders',
            'create-orders',
        ]);

        return response()->json([
            'access_token' => $token->accessToken,
            'token_type' => 'Bearer',
            'expires_at' => $token->token->expires_at,
            // Personal access tokens don't have refresh tokens
            // Use authorization code grant with PKCE for refresh token support
        ]);
    }

    /**
     * Revoke access and refresh tokens.
     */
    public function logout(Request $request)
    {
        $tokenId = $request->user()->token()->id;

        // Revoke access token
        app(TokenRepository::class)->revokeAccessToken($tokenId);

        // Revoke all refresh tokens for this access token
        app(RefreshTokenRepository::class)->revokeRefreshTokensByAccessTokenId($tokenId);

        return response()->json([
            'message' => 'Successfully logged out',
        ]);
    }
}
```

### Passport OAuth2 Client Credentials Grant

For machine-to-machine authentication where no user context is needed:

```php
<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;

class MachineToMachineController extends Controller
{
    /**
     * Endpoint protected by client credentials middleware.
     * Route: Route::get('/api/reports', [MachineToMachineController::class, 'index'])
     *            ->middleware('client:generate-reports');
     */
    public function generateReport(Request $request)
    {
        // This endpoint is accessed by other services, not users
        // Authentication is via client_id and client_secret

        $report = $this->compileSystemReport();

        return response()->json([
            'generated_at' => now()->toISOString(),
            'report' => $report,
        ]);
    }

    private function compileSystemReport(): array
    {
        return [
            'total_users' => \App\Models\User::count(),
            'active_subscriptions' => \App\Models\Subscription::where('status', 'active')->count(),
            'revenue_mtd' => \App\Models\Payment::whereMonth('created_at', now()->month)->sum('amount'),
        ];
    }
}
```

### Passport Scopes Configuration

```php
<?php

namespace App\Providers;

use Illuminate\Support\ServiceProvider;
use Laravel\Passport\Passport;

class AuthServiceProvider extends ServiceProvider
{
    public function boot(): void
    {
        // Define available OAuth2 scopes
        Passport::tokensCan([
            'read-profile' => 'Read user profile information',
            'update-profile' => 'Update user profile',
            'read-orders' => 'View order history',
            'create-orders' => 'Create new orders',
            'admin' => 'Full administrative access',
            'generate-reports' => 'Generate system reports (machine-to-machine)',
        ]);

        // Set default scopes when none specified
        Passport::setDefaultScope([
            'read-profile',
        ]);

        // Token lifetimes
        Passport::tokensExpireIn(now()->addDays(15));
        Passport::refreshTokensExpireIn(now()->addDays(30));
        Passport::personalAccessTokensExpireIn(now()->addMonths(6));
    }
}
```

### Authorization Code Grant with PKCE

For third-party applications and SPAs, the authorization code grant with PKCE is the recommended approach:

```php
<?php

// routes/web.php - OAuth2 authorization routes
use Illuminate\Support\Facades\Route;

// Passport automatically registers these routes, but here's what they do:
// GET  /oauth/authorize - Display authorization form
// POST /oauth/authorize - Approve authorization request
// POST /oauth/token     - Issue access token
// POST /oauth/token/refresh - Refresh access token

// Custom approval page (optional)
Route::get('/oauth/authorize', function () {
    // Passport handles this, but you can customize the view
    return view('passport.authorize');
})->middleware(['web', 'auth']);
```

```javascript
// Third-party application implementing PKCE flow
async function initiateOAuthFlow() {
    // Generate PKCE code verifier and challenge
    const codeVerifier = generateRandomString(128);
    const codeChallenge = await sha256Base64Url(codeVerifier);
    
    // Store verifier for later use
    sessionStorage.setItem('code_verifier', codeVerifier);
    
    // Redirect to authorization server
    const authUrl = new URL('https://api.example.com/oauth/authorize');
    authUrl.searchParams.set('client_id', 'your-client-id');
    authUrl.searchParams.set('redirect_uri', 'https://your-app.com/callback');
    authUrl.searchParams.set('response_type', 'code');
    authUrl.searchParams.set('scope', 'read-profile read-orders');
    authUrl.searchParams.set('code_challenge', codeChallenge);
    authUrl.searchParams.set('code_challenge_method', 'S256');
    authUrl.searchParams.set('state', generateRandomString(32));
    
    window.location.href = authUrl.toString();
}

async function handleCallback(authorizationCode) {
    const codeVerifier = sessionStorage.getItem('code_verifier');
    
    // Exchange authorization code for tokens
    const response = await fetch('https://api.example.com/oauth/token', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            grant_type: 'authorization_code',
            client_id: 'your-client-id',
            redirect_uri: 'https://your-app.com/callback',
            code: authorizationCode,
            code_verifier: codeVerifier,
        }),
    });
    
    const tokens = await response.json();
    // tokens.access_token, tokens.refresh_token, tokens.expires_in
    return tokens;
}

function generateRandomString(length) {
    const array = new Uint8Array(length);
    crypto.getRandomValues(array);
    return Array.from(array, byte => byte.toString(16).padStart(2, '0')).join('');
}

async function sha256Base64Url(str) {
    const encoder = new TextEncoder();
    const data = encoder.encode(str);
    const hash = await crypto.subtle.digest('SHA-256', data);
    return btoa(String.fromCharCode(...new Uint8Array(hash)))
        .replace(/\+/g, '-')
        .replace(/\//g, '_')
        .replace(/=+$/, '');
}
```

## Side-by-Side Comparison

| Feature | Sanctum | Passport |
|---------|---------|----------|
| **Primary Use Case** | First-party apps, SPAs | Third-party OAuth2 access |
| **Token Storage** | Database (simple) | Database (OAuth2 tables) |
| **OAuth2 Support** | No | Full implementation |
| **SPA Cookie Auth** | Yes (stateful) | No |
| **Mobile App Support** | Yes (tokens) | Yes (tokens) |
| **Third-Party Access** | No | Yes |
| **Token Scopes** | Abilities (simple) | OAuth2 Scopes |
| **Setup Complexity** | Minimal | Moderate |
| **Database Migrations** | 1 table | 5+ tables |
| **Token Refresh** | Manual revoke/create | Built-in refresh tokens |

## Testing the Implementation

```php
<?php

namespace Tests\Feature;

use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Laravel\Sanctum\Sanctum;
use Tests\TestCase;

class ApiAuthenticationTest extends TestCase
{
    use RefreshDatabase;

    public function test_sanctum_token_authentication(): void
    {
        $user = User::factory()->create();

        // Create token with specific abilities
        $token = $user->createToken('test-token', ['read:profile']);

        $response = $this->withHeaders([
            'Authorization' => 'Bearer ' . $token->plainTextToken,
        ])->getJson('/api/user');

        $response->assertOk()
            ->assertJsonStructure(['id', 'name', 'email']);
    }

    public function test_sanctum_acting_as_user(): void
    {
        $user = User::factory()->create();

        // Use Sanctum's actingAs helper for cleaner tests
        Sanctum::actingAs($user, ['read:profile', 'read:orders']);

        $response = $this->getJson('/api/orders');

        $response->assertOk();
    }

    public function test_token_abilities_are_enforced(): void
    {
        $user = User::factory()->create();

        // Token without required ability
        Sanctum::actingAs($user, ['read:profile']);

        $response = $this->postJson('/api/orders', [
            'items' => [['product_id' => 1, 'quantity' => 1]],
        ]);

        $response->assertForbidden();
    }

    public function test_unauthenticated_requests_are_rejected(): void
    {
        $response = $this->getJson('/api/user');

        $response->assertUnauthorized();
    }

    public function test_token_revocation(): void
    {
        $user = User::factory()->create();
        $token = $user->createToken('test-token');

        // First request succeeds
        $this->withHeaders([
            'Authorization' => 'Bearer ' . $token->plainTextToken,
        ])->getJson('/api/user')->assertOk();

        // Revoke the token
        $user->tokens()->delete();

        // Subsequent request fails
        $this->withHeaders([
            'Authorization' => 'Bearer ' . $token->plainTextToken,
        ])->getJson('/api/user')->assertUnauthorized();
    }
}
```

### Passport-Specific Tests

```php
<?php

namespace Tests\Feature;

use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Laravel\Passport\Passport;
use Tests\TestCase;

class PassportAuthenticationTest extends TestCase
{
    use RefreshDatabase;

    public function test_passport_scopes_are_enforced(): void
    {
        $user = User::factory()->create();

        // Create token with specific scopes
        Passport::actingAs($user, ['read-profile']);

        // Attempt to access endpoint requiring different scope
        $response = $this->getJson('/api/admin/users');

        $response->assertForbidden();
    }

    public function test_client_credentials_grant(): void
    {
        // Create OAuth client
        $client = \Laravel\Passport\Client::factory()->create([
            'personal_access_client' => false,
            'password_client' => false,
            'revoked' => false,
        ]);

        // Request token using client credentials
        $response = $this->postJson('/oauth/token', [
            'grant_type' => 'client_credentials',
            'client_id' => $client->id,
            'client_secret' => $client->secret,
            'scope' => 'generate-reports',
        ]);

        $response->assertOk()
            ->assertJsonStructure([
                'token_type',
                'expires_in',
                'access_token',
            ]);
    }
}
```

## Decision Framework

Use this framework to choose the right package:

### Choose Sanctum When:

1. **You control both frontend and backend** - Your SPA/mobile app is first-party
2. **Simple token authentication suffices** - No OAuth2 requirements
3. **Cookie-based SPA auth is preferred** - Same-domain applications
4. **Minimal setup is important** - Quick time-to-market
5. **No third-party API access needed** - Internal applications only

### Choose Passport When:

1. **Third-party applications need API access** - Building a platform/marketplace
2. **OAuth2 compliance is required** - Enterprise integrations
3. **Machine-to-machine auth is needed** - Microservices architecture
4. **Token refresh is critical** - Long-lived sessions with security
5. **Multiple grant types required** - Complex authentication flows

## Conclusion

Both Laravel Sanctum and Passport solve API authentication, but for fundamentally different use cases. Sanctum excels in simplicity for first-party applications where you control the entire stack. Passport provides the full OAuth2 implementation necessary for third-party access and complex enterprise integrations.

The right choice depends on your specific requirements:

- **Reduced complexity**: Sanctum's lightweight approach minimizes maintenance overhead
- **Third-party ecosystem**: Passport enables building platforms that external developers can integrate with
- **Security compliance**: Passport's OAuth2 implementation satisfies enterprise security requirements
- **Development velocity**: Sanctum's simpler setup accelerates initial development

For most Laravel applications serving their own frontends, Sanctum provides the optimal balance of security and simplicity. Reserve Passport for scenarios requiring full OAuth2 server capabilities or third-party API access.

**Need help choosing the right authentication strategy for your Laravel API?** Let's discuss your specific requirements and design an authentication architecture that scales with your business needs while maintaining security best practices.
