import type { Collection } from "tinacms";

export const WorkCollection: Collection = {
  name: "work",
  label: "Work",
  path: "src/content/work",
  format: "mdx",
  ui: {
    router({ document }) {
      return `/work/${document._sys.filename}`;
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
      name: "artworks",
      label: "Artworks",
      type: "object",
      list: true,
      fields: [
        {
          name: "image",
          label: "Image",
          type: "image",
        },
        {
          name: "caption",
          label: "Caption",
          type: "string",
        },
      ],
    },
    {
      type: "rich-text",
      name: "body",
      label: "Body",
      isBody: true,
    },
  ],
};
