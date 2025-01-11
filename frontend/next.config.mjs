import URLManagement from '@/utils/URLManagement';

const url = URLManagement();

/** @type {import('next').NextConfig} */
const nextConfig = {

    async rewrites() {
      return [
        {
          source: "/api/:path*/",
          destination: `${url}/api/:path*/`,
        },
        {
          source: "/media/:path*/",
          destination: `${url}/media/:path*/`,
        },
      ];
    },
    trailingSlash: true,
  };
  
  export default nextConfig;