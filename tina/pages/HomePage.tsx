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

  return (
    <main>
      {page.heroImage && (
        <div data-tina-field={tinaField(page, "heroImage")}>
          <img src={page.heroImage} alt="" />
        </div>
      )}
      <div data-tina-field={tinaField(page, "body")} className="prose">
        <TinaMarkdown content={page.body} />
      </div>
    </main>
  );
};

export default HomePage;
