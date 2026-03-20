import { SignIn } from '@clerk/nextjs';
import { hasClerkEnv } from '../../../lib/clerk-env';

export default function SignInPage() {
  if (!hasClerkEnv()) {
    return (
      <main>
        <h1>Sign in</h1>
        <p>Clerk isn&apos;t configured yet. Add `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` and `CLERK_SECRET_KEY` to enable sign-in.</p>
      </main>
    );
  }

  return (
    <main>
      <h1>Sign in</h1>
      <SignIn />
    </main>
  );
}
