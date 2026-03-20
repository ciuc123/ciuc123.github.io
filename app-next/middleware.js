import { clerkMiddleware, createRouteMatcher } from '@clerk/nextjs/server';
import { hasClerkEnv } from './lib/clerk-env';

const isProtectedRoute = createRouteMatcher(['/library(.*)']);

export default clerkMiddleware(async (auth, req) => {
  if (!hasClerkEnv()) {
    return;
  }

  if (isProtectedRoute(req)) {
    await auth.protect();
  }
});

export const config = {
  matcher: ['/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)', '/(api|trpc)(.*)']
};
