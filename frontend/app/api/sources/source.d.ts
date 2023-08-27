export type Source = {
  summarized: string;
  thread_id: string;
  thread_link: string;
};

export type Sources = {
  query: string;
  threads: Source[];
};

export type SourcesList = Sources[];

export type SourcesMap = {
  [userId: string]: SourcesList;
};
