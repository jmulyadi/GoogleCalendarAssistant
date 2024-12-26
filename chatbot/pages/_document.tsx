import { Html, Head, Main, NextScript } from "next/document";

export default function Document() {
  return (
    <Html lang="en">
      <Head />
      <body className="bg-white text-black dark:bg-background dark:text-textPrimary dark:border-border">
        <script
          dangerouslySetInnerHTML={{
            __html: `
              if (
                localStorage.theme === 'dark' ||
                (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)
              ) {
                document.documentElement.classList.add('dark');
              } else {
                document.documentElement.classList.remove('dark');
              }
            `,
          }}
        />
        <Main />
        <NextScript />
      </body>
    </Html>
  );
}
