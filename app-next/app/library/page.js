import { auth } from '@clerk/nextjs/server';
import { redirect } from 'next/navigation';
import { hasClerkEnv } from '../../lib/clerk-env';

export default async function LibraryPage() {
  if (!hasClerkEnv()) {
    return (
      <main>
        <h1>Library</h1>
        <p>Clerk isn&apos;t configured yet. Add `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` and `CLERK_SECRET_KEY` to enable protected access.</p>
      </main>
    );
  }

  const { userId } = await auth();

  if (!userId) {
    redirect('/sign-in?redirect_url=/library');
  }

  return (
    <main>
      <h1>Library</h1>
      <p>Protected placeholder route for upcoming content migration.</p>
      <p><strong>Clerk user id:</strong> {userId}</p>
    </main>
  );
}
