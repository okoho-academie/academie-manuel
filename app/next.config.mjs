/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Les contenus (séances, structure) sont lus depuis le dépôt parent au moment du build.
  outputFileTracingIncludes: { '/seance/[code]': ['../seances/**/*'], '/parcours': ['../manuel/**/*'] },
};
export default nextConfig;
