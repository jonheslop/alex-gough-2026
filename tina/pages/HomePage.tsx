import { tinaField, useTina } from "tinacms/dist/react";
import type { PageQuery, PageQueryVariables } from "../__generated__/types";
import { TinaMarkdown } from "tinacms/dist/rich-text";

type Props = {
  variables: PageQueryVariables;
  data: PageQuery;
  query: string;
};

const HomePage = (props: Props) => {
  const { data } = useTina({
    query: props.query,
    variables: props.variables,
    data: props.data,
  });

  const page = data.page;
  const heroImages = page.heroImages ?? [];

  return (
    <main>
      <div data-tina-field={tinaField(page, "body")} className="prose">
        <TinaMarkdown content={page.body} />
      </div>
      {heroImages.length > 0 && (
        <div
          className="slideshow"
          data-tina-field={tinaField(page, "heroImages")}
        >
          {heroImages.map((image, index) => (
            <img
              key={image.image}
              className="slideshow-slide"
              src={image.image}
              alt={image.caption ?? ""}
              data-active={index === 0 ? "" : undefined}
            />
          ))}
        </div>
      )}
    </main>
  );
};

export default HomePage;
