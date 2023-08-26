export type Sources = {
  summarized: string;
  thread_id: string;
  thread_link: string;
}[];

export type SourceMap = {
  [userId: string]: Sources;
}
