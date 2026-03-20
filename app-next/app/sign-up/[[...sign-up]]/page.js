import { SignUp } from '@clerk/nextjs';
import { hasClerkEnv } from '../../../lib/clerk-env';

export default function SignUpPage() {
  if (!hasClerkEnv()) {
    return (
      <main>
        <h1>Sign up</h1>
        <p>Clerk isn&apos;t configured yet. Add `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` and `CLERK_SECRET_KEY` to enable sign-up.</p>
      </main>
    );
  }

  return (
    <main>
      <h1>Sign up</h1>
      <SignUp />
    </main>
  );
}
