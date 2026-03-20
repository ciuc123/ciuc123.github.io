import { SignIn } from '@clerk/nextjs';

export default function SignInPage() {
  return (
    <main>
      <h1>Sign in</h1>
      <SignIn />
    </main>
  );
}

