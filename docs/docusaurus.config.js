// @ts-check
// `@type` JSDoc annotations allow editor autocompletion and type checking
// (when paired with `@ts-check`).
// There are various equivalent ways to declare your Docusaurus config.
// See: https://docusaurus.io/docs/api/docusaurus-config

import {themes as prismThemes} from 'prism-react-renderer';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'SpiceCode | Documentation',
  tagline: 'The next generation of code analysis.',
  favicon: 'img/spicecode_logo_nobg.png',

  // Set the production url of your site here
  url: 'https://spicecodecli.github.io', // Assuming deployment to GitHub Pages
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/spicecode/', // Base URL for GitHub pages deployment

  // GitHub pages deployment config.
  organizationName: 'spicecodecli', // Your GitHub org/user name.
  projectName: 'spicecode', // Usually your repo name for the docs site. (im guessing since we dont have a docs repo we can just use the regular repo here?)

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  // my site is not chinese. but thank you for the heads up
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'pt-br'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          // Point to the actual SpiceCode repo for edits
          editUrl:
            'https://github.com/spicecodecli/spicecode/tree/main/docs', // Link to the source repo, assuming docs might live there eventually or for context
        },
        blog: false, // Disabling blog as it wasn't requested // WAIT WE CAN HAVE A BLOG HERE??????????????? // TODO: RESEARCH BLOG POSSIBILITIES
        // blog: {
        //   showReadingTime: true,
        //   feedOptions: {
        //     type: ['rss', 'atom'],
        //     xslt: true,
        //   },
        //   // Please change this to your repo.
        //   // Remove this to remove the "edit this page" links.
        //   editUrl:
        //     'https://github.com/spicecodecli/spicecode/tree/main/',
        //   // Useful options to enforce blogging best practices
        //   onInlineTags: 'warn',
        //   onInlineAuthors: 'warn',
        //   onUntruncatedBlogPosts: 'warn',
        // },
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Replace with your project's social card // what even is a social card?
      image: 'img/spicecode_wallpaper.png', // Placeholder social card
      navbar: {
        title: 'SpiceCode',
        logo: {
          alt: 'SpiceCode Logo',
          src: 'img/spicecode_logo_nobg.png', // Assuming a logo will be added later
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'docsSidebar', // Updated sidebar ID
            position: 'left',
            label: 'Documentation',
          },
          {
          type: 'localeDropdown',
          position: 'left',
        },
          // {to: '/blog', label: 'Blog', position: 'left'}, // Blog disabled
          {
            href: 'https://github.com/spicecodecli/spicecode',
            label: 'GitHub',
            position: 'right',
          },
          
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Docs',
            items: [
              {
                label: 'Introduction',
                to: '/docs/intro',
              },
              {
                label: 'Installation',
                to: '/docs/getting-started/installation',
              },
              {
                label: 'Usage',
                to: '/docs/usage/cli',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              // Add relevant community links if they exist
              // {
              //   label: 'Stack Overflow',
              //   href: 'https://stackoverflow.com/questions/tagged/spicecode',
              // },
              // {
              //   label: 'Discord',
              //   href: 'https://discordapp.com/invite/your-invite',
              // },
              {
                label: 'Report an Issue',
                href: 'https://github.com/spicecodecli/spicecode/issues',
              },
              {
                label: 'GitHub Discussions',
                href: 'https://github.com/orgs/spicecodecli/discussions',
              },
            ],
          },
          {
            title: 'More',
            items: [
              // { label: 'Blog', to: '/blog' }, // Blog disabled
              {
                label: 'GitHub',
                href: 'https://github.com/spicecodecli/spicecode',
              },
            ],
          },
        ],
        // Update copyright notice
        copyright: `Copyright © ${new Date().getFullYear()} SpiceCode CLI. Built with Docusaurus.`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
        // Add language support for Go, Python, Ruby, JavaScript if not default
        additionalLanguages: ['go', 'ruby'],
      },
    }),
};

export default config;

