---
layout: post
title: "From Broken Tests to Bulletproof Code: Laravel Testing Strategies That Actually Work"
date: 2025-10-22
---

Testing is the difference between code that works now and code that keeps working. Yet most Laravel projects have either no tests or tests that break every time someone refactors. After managing multiple large Laravel codebases and hiring dozens of developers, I've learned that good testing isn't about coverage percentages--it's about confidence and speed.

## Why Testing Matters for Your Bottom Line

When tech leads evaluate developers, they look for those who ship reliable code fast. Testing enables both. A solid test suite means faster code reviews, fewer production hotfixes, and the confidence to refactor without fear. For hiring managers, developers who write good tests cost less in the long run--they create fewer bugs and enable the team to move faster.

## The Problem with Traditional Testing Approaches

Most Laravel projects fall into one of three categories:

**No tests:** "We'll add them later." Later never comes, and every deployment is a gamble[21][24].

**Brittle tests:** Tests break with every minor refactoring. Eventually, developers stop running them or delete them[27].

**False confidence:** High coverage but tests that don't actually verify behavior. They pass even when the code is broken[30].

The real issue? Testing tutorials focus on syntax, not strategy. They show you how to write a test, not what to test or how to structure tests that survive refactoring.

## Solution: Three Testing Strategies That Actually Work

### Strategy 1: Feature Tests Over Unit Tests

Controversial take: Most Laravel applications need fewer unit tests and more feature tests. Unit tests break during refactoring because they're coupled to implementation details. Feature tests verify behavior from the user's perspective[21][27].

**Bad: Unit test coupled to implementation**
```php
public function test_user_service_creates_user()
{
    $service = new UserService();
    $user = $service->createUser([
        'name' => 'John Doe',
        'email' => 'john@example.com'
    ]);
    
    $this->assertInstanceOf(User::class, $user);
    // Breaks if you rename UserService or change its constructor
}
```

**Good: Feature test verifying behavior**
```php
public function test_user_can_register_successfully()
{
    $response = $this->post('/register', [
        'name' => 'John Doe',
        'email' => 'john@example.com',
        'password' => 'password123',
        'password_confirmation' => 'password123'
    ]);
    
    $response->assertRedirect('/dashboard');
    $this->assertDatabaseHas('users', [
        'email' => 'john@example.com'
    ]);
    
    // Survives refactoring as long as behavior stays the same
}
```

**When to use each:**
- **Feature tests:** API endpoints, user workflows, critical business logic (80% of tests)
- **Unit tests:** Complex algorithms, utility functions, pure functions (20% of tests)

### Strategy 2: Use Database Transactions, Not RefreshDatabase

The standard Laravel testing advice is to use `RefreshDatabase` trait. But for large applications, this is painfully slow. Each test drops and recreates your entire database schema[25].

**Slow approach (adds 500ms+ per test):**
```php
use Illuminate\Foundation\Testing\RefreshDatabase;

class UserTest extends TestCase
{
    use RefreshDatabase; // Migrates database before EVERY test
    
    public function test_user_can_login()
    {
        // Test runs 500ms+ slower due to migrations
    }
}
```

**Fast approach (adds ~10ms per test):**
```php
use Illuminate\Foundation\Testing\DatabaseTransactions;

class UserTest extends TestCase
{
    use DatabaseTransactions; // Rolls back after each test
    
    public function test_user_can_login()
    {
        // Test runs near-instantly
    }
}
```

**The trade-off:** `DatabaseTransactions` wraps each test in a transaction and rolls it back. This is 50x faster but doesn't work for tests that need to verify transaction behavior or commit hooks[25].

**My rule:** Use `DatabaseTransactions` for 95% of tests. Use `RefreshDatabase` only when specifically testing database-level features.

### Strategy 3: Prevent External API Calls with HTTP Fakes

Nothing kills CI/CD speed like tests making real HTTP requests. They're slow, flaky, and can rack up API costs. Laravel's HTTP fake is the solution[25].

**Problem: Real API calls in tests**
```php
public function test_payment_processing()
{
    $response = $this->post('/checkout', [
        'amount' => 100.00
    ]);
    
    // This test actually charges Stripe $100.00
    // Slow, costs money, fails if API is down
}
```

**Solution: Mock external services**
```php
use Illuminate\Support\Facades\Http;

public function test_payment_processing()
{
    Http::fake([
        'api.stripe.com/*' => Http::response([
            'id' => 'ch_test123',
            'status' => 'succeeded'
        ], 200)
    ]);
    
    $response = $this->post('/checkout', [
        'amount' => 100.00
    ]);
    
    $response->assertSuccessful();
    
    Http::assertSent(function ($request) {
        return $request->url() === 'https://api.stripe.com/charges' &&
               $request['amount'] === 10000;
    });
}
```

**Bonus: Catch stray requests**
```php
Http::preventStrayRequests(); // Fails if any unmocked request is made
```

This catches tests that accidentally hit real APIs, preventing both flakiness and surprise bills[25].

## Code Implementation: Building a Bulletproof Test Suite

Let's implement a complete testing setup for a Laravel e-commerce application:

```php
<?php

namespace Tests\Feature;

use Tests\TestCase;
use App\Models\User;
use App\Models\Product;
use Illuminate\Foundation\Testing\DatabaseTransactions;
use Illuminate\Support\Facades\Http;

class CheckoutTest extends TestCase
{
    use DatabaseTransactions;
    
    protected function setUp(): void
    {
        parent::setUp();
        
        // Prevent any unmocked HTTP requests
        Http::preventStrayRequests();
        
        // Set up common test data
        $this->user = User::factory()->create();
        $this->product = Product::factory()->create([
            'price' => 100.00,
            'stock' => 10
        ]);
    }
    
    public function test_user_can_complete_checkout_successfully()
    {
        // Arrange: Mock payment gateway
        Http::fake([
            'api.stripe.com/v1/charges' => Http::response([
                'id' => 'ch_test123',
                'status' => 'succeeded',
                'amount' => 10000
            ], 200)
        ]);
        
        // Act: User completes checkout
        $response = $this->actingAs($this->user)
            ->post('/checkout', [
                'product_id' => $this->product->id,
                'quantity' => 1,
                'payment_method' => 'stripe'
            ]);
        
        // Assert: Verify behavior
        $response->assertRedirect('/orders');
        
        // Verify order was created
        $this->assertDatabaseHas('orders', [
            'user_id' => $this->user->id,
            'product_id' => $this->product->id,
            'total' => 100.00,
            'status' => 'completed'
        ]);
        
        // Verify inventory was reduced
        $this->assertEquals(9, $this->product->fresh()->stock);
        
        // Verify Stripe was called correctly
        Http::assertSent(function ($request) {
            return $request->url() === 'https://api.stripe.com/v1/charges' &&
                   $request['amount'] === 10000 &&
                   $request['currency'] === 'usd';
        });
    }
    
    public function test_checkout_fails_when_payment_declined()
    {
        // Arrange: Mock declined payment
        Http::fake([
            'api.stripe.com/v1/charges' => Http::response([
                'error' => [
                    'type' => 'card_error',
                    'message' => 'Your card was declined'
                ]
            ], 402)
        ]);
        
        $initialStock = $this->product->stock;
        
        // Act
        $response = $this->actingAs($this->user)
            ->post('/checkout', [
                'product_id' => $this->product->id,
                'quantity' => 1,
                'payment_method' => 'stripe'
            ]);
        
        // Assert: Order not created
        $this->assertDatabaseMissing('orders', [
            'user_id' => $this->user->id,
            'status' => 'completed'
        ]);
        
        // Inventory unchanged
        $this->assertEquals($initialStock, $this->product->fresh()->stock);
        
        // User sees error
        $response->assertSessionHasErrors('payment');
    }
    
    public function test_checkout_prevents_overselling()
    {
        // Arrange: Product with limited stock
        $this->product->update(['stock' => 1]);
        
        Http::fake([
            'api.stripe.com/*' => Http::response(['status' => 'succeeded'], 200)
        ]);
        
        // Act: Try to buy more than available
        $response = $this->actingAs($this->user)
            ->post('/checkout', [
                'product_id' => $this->product->id,
                'quantity' => 2,
                'payment_method' => 'stripe'
            ]);
        
        // Assert: Order rejected
        $response->assertStatus(422);
        $response->assertJsonValidationErrors('quantity');
        
        // No charge attempted
        Http::assertNothingSent();
    }
}
```

## Testing: Verify Your Test Suite Quality

Run these commands to ensure your tests are reliable:

```bash
# Run tests with coverage
php artisan test --coverage

# Run tests in parallel (faster)
php artisan test --parallel

# Run only feature tests
php artisan test --testsuite=Feature

# Run with strict mode (fails on warnings)
php artisan test --stop-on-failure

# Profile slow tests
php artisan test --profile
```

**Good test suite indicators:**
- ✓ Tests run in under 30 seconds
- ✓ No real external API calls
- ✓ Tests pass consistently (no flaky tests)
- ✓ Code coverage above 70% for business logic
- ✓ Tests survive refactoring

**Bad indicators:**
- ✗ Tests take minutes to run
- ✗ Tests fail randomly
- ✗ Tests require manual database setup
- ✗ Tests break after minor code changes

## Conclusion: From Fear to Confidence

Good tests aren't about hitting coverage numbers--they're about enabling your team to ship faster with confidence. When tests are fast, reliable, and focused on behavior rather than implementation, developers actually run them. When they run them, they catch bugs before production.

**The transformation:**
- **Before:** Developers afraid to refactor, manual QA for every change, production bugs
- **After:** Confident refactoring, fast deployments, bugs caught in CI/CD

For hiring managers: Ask candidates about their testing strategy. Good developers don't just know how to write tests--they know what to test, how to structure tests for speed, and how to mock external dependencies effectively.

For tech leads: Invest in test infrastructure. Fast, reliable tests pay dividends in deployment speed and developer happiness. A test suite that runs in 30 seconds gets used. One that takes 10 minutes gets skipped.

**Ready to transform your test suite?** Start with database transactions and HTTP fakes. These two changes alone can speed up tests by 10-50x.

---

**Need a Laravel developer who builds bulletproof test suites?** I'm available for backend roles where code quality and reliability aren't optional. Let's talk.