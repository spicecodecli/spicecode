// @ts-check

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.

 @type {import("@docusaurus/plugin-content-docs").SidebarsConfig}
 */
const sidebars = {
  // Define the main documentation sidebar
  docsSidebar: [
    // Link to the introductory page
    "intro",
    // Getting Started Category
    {
      type: "category",
      label: "Getting Started",
      items: [
        "getting-started/installation",
        "getting-started/quick-start",
      ],
    },
    // Usage Guide Category
    {
      type: "category",
      label: "Usage Guide",
      items: [
        "usage/cli",
        "usage/analyzers",
      ],
    },
    // Supported Languages Category
    {
      type: "category",
      label: "Supported Languages",
      items: [
        "languages/go",
        "languages/javascript",
        "languages/python",
        "languages/ruby",
      ],
    },
    // API Reference Category
    {
      type: "category",
      label: "API Reference",
      items: [
        "api/lexers",
        "api/parser",
        "api/analyzers",
        "api/utils",
      ],
    },
    // Architecture Overview Page
    "architecture",
    // Contributing Page (Updated)
    "contributing/guidelines",
  ],
};

export default sidebars;

