export const metadata = {
  title: "Ciuculescu Next Foundation",
  description: "Initial Next.js App Router foundation for migration."
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body style={{ fontFamily: "system-ui, sans-serif", margin: 24 }}>
        {children}
      </body>
    </html>
  );
}

