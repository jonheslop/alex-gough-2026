import type { Collection } from "tinacms";

export const PortfolioCollection: Collection = {
  name: "portfolio",
  label: "Portfolio",
  path: "src/content/portfolio",
  format: "mdx",
  ui: {
    router({ document }) {
      return `/portfolio/${document._sys.filename}`;
    },
  },
  fields: [
    {
      type: "string",
      name: "title",
      label: "Title",
      isTitle: true,
      required: true,
    },
    {
      name: "description",
      label: "Description",
      type: "string",
    },
    {
      name: "pubDate",
      label: "Publication Date",
      type: "datetime",
    },
    {
      name: "updatedDate",
      label: "Updated Date",
      type: "datetime",
    },
    {
      name: "heroImage",
      label: "Hero Image",
      type: "image",
    },
    {
      label: "Category",
      name: "category",
      type: "reference",
      collections: ["category"],
    },
    {
      type: "rich-text",
      name: "body",
      label: "Body",
      isBody: true,
    },
  ],
};
