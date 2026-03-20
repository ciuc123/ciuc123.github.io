import { auth } from '@clerk/nextjs/server';
import { redirect } from 'next/navigation';

export default async function LibraryPage() {
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
