import type { Collection } from "tinacms";

export const PageCollection: Collection = {
  name: "page",
  label: "Pages",
  path: "src/content/page",
  format: "mdx",
  ui: {
    router: ({ document }) => {
      return `/${document._sys.filename}`;
    },
  },
  fields: [
    {
      name: "seoTitle",
      type: "string",
      required: true,
    },
    {
      name: "heroImages",
      label: "Hero Images",
      type: "object",
      list: true,
      fields: [
        {
          name: "image",
          type: "image",
          required: true,
        },
        {
          name: "caption",
          type: "string",
        },
      ],
    },
    {
      name: "body",
      type: "rich-text",
      isBody: true,
      required: true,
    },
  ],
};
