import { ClerkProvider, SignedIn, SignedOut, UserButton } from '@clerk/nextjs';

export const metadata = {
  title: "Ciuculescu Next Foundation",
  description: "Initial Next.js App Router foundation for migration."
};

export default function RootLayout({ children }) {
  return (
    <ClerkProvider>
      <html lang="en">
        <body style={{ fontFamily: "system-ui, sans-serif", margin: 24 }}>
          <header style={{ display: "flex", gap: 16, alignItems: "center", marginBottom: 24 }}>
            <a href="/">Home</a>
            <a href="/library">Library</a>
            <SignedOut>
              <a href="/sign-in">Sign in</a>
              <a href="/sign-up">Sign up</a>
            </SignedOut>
            <SignedIn>
              <UserButton />
            </SignedIn>
          </header>
          {children}
        </body>
      </html>
    </ClerkProvider>
  );
}
