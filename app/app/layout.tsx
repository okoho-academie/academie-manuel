import type { Metadata, Viewport } from 'next';
import localFont from 'next/font/local';
import './globals.css';
import { Entete } from '@/components/Entete';
import { Pied } from '@/components/Pied';

// Polices embarquées (Google Fonts n'est pas joignable depuis l'environnement de build).
const montserrat = localFont({ src: '../fonts/Montserrat-Variable.ttf', variable: '--font-display', weight: '100 900', display: 'swap' });
const openSans = localFont({ src: '../fonts/OpenSans-Variable.ttf', variable: '--font-body', weight: '300 800', display: 'swap' });

export const metadata: Metadata = {
  title: { default: 'OKOHO Académie', template: '%s · OKOHO Académie' },
  description: "De l'idée au service digital vendu, avec Claude. Une formation OKOHO Consulting GmbH.",
  manifest: '/manifest.webmanifest',
  icons: { icon: '/icons/icon-192.png', apple: '/icons/icon-192.png' },
};
export const viewport: Viewport = { themeColor: '#0E4A7B', width: 'device-width', initialScale: 1, viewportFit: 'cover' };

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="fr" className={`${montserrat.variable} ${openSans.variable}`}>
      <body>
        <Entete />
        <main>{children}</main>
        <Pied />
      </body>
    </html>
  );
}
