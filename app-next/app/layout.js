import { ClerkProvider, SignedIn, SignedOut, UserButton } from '@clerk/nextjs';
import { hasClerkEnv } from '../lib/clerk-env';

export const metadata = {
  title: "Ciuculescu Next Foundation",
  description: "Initial Next.js App Router foundation for migration."
};

export default function RootLayout({ children }) {
  const clerkEnabled = hasClerkEnv();

  const content = (
    <>
      <header style={{ display: "flex", gap: 16, alignItems: "center", marginBottom: 24 }}>
        <a href="/">Home</a>
        <a href="/library">Library</a>
        {clerkEnabled ? (
          <>
            <SignedOut>
              <a href="/sign-in">Sign in</a>
              <a href="/sign-up">Sign up</a>
            </SignedOut>
            <SignedIn>
              <UserButton />
            </SignedIn>
          </>
        ) : (
          <span style={{ color: "#666" }}>Clerk env vars not configured</span>
        )}
      </header>
      {children}
    </>
  );

  return (
    <html lang="en">
      <body style={{ fontFamily: "system-ui, sans-serif", margin: 24 }}>
        {clerkEnabled ? <ClerkProvider>{content}</ClerkProvider> : content}
      </body>
    </html>
  );
}
