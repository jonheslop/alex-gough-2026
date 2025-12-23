import React from "react";
import { tinaField, useTina } from "tinacms/dist/react";
import type { WorkQuery, WorkQueryVariables } from "../__generated__/types";
import { TinaMarkdown } from "tinacms/dist/rich-text";
import FormattedDate from "../../src/components/react/FormattedDate.tsx";

type Props = {
  variables: WorkQueryVariables;
  data: WorkQuery;
  query: string;
};

export default function AdminBlogPost(props: Props) {
  const { data } = useTina({
    query: props.query,
    variables: props.variables,
    data: props.data,
  });

  const work = data.work;

  return (
    <article>
      <div
        data-tina-field={tinaField(work, "heroImage")}
        className="hero-image"
      >
        {work.heroImage && (
          <img width={1020} height={510} src={work.heroImage} alt="" />
        )}
      </div>
      <div className="prose">
        <div className="title">
          <div className="date" data-tina-field={tinaField(work, "pubDate")}>
            <FormattedDate date={work.pubDate} />
            {work.updatedDate && (
              <div
                className="last-updated-on"
                data-tina-field={tinaField(work, "updatedDate")}
              >
                Last updated on <FormattedDate date={work.updatedDate} />
              </div>
            )}
          </div>
          <h1 data-tina-field={tinaField(work, "title")}>{work.title}</h1>
          <hr />
        </div>
        <div data-tina-field={tinaField(work, "body")}>
          <TinaMarkdown content={work.body} />
        </div>
      </div>
    </article>
  );
}
