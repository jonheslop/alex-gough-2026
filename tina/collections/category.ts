import type { Collection } from "tinacms";

export const CategoryCollection: Collection = {
  name: "category",
  label: "Categories",
  path: "src/content/category",
  fields: [
    {
      type: "string",
      name: "name",
      label: "Name",
      isTitle: true,
      required: true,
    },
    {
      type: "string",
      name: "description",
      label: "Description",
      ui: {
        component: "textarea",
      },
    },
  ],
};
