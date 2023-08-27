import { SourcesMap } from './sources/source';
import { User } from './users/user';

export const DEFAULT_USERS = [
  {
    id: 'USLACKBOT',
    name: 'slackbot',
    profile_pic: 'https://a.slack-edge.com/80588/img/slackbot_32.png',
  },
  {
    id: 'U05P8LXRC9M',
    name: 'steven.xu1589',
    profile_pic:
      'https://avatars.slack-edge.com/2023-08-26/5805544754466_9eae1a406e26088ec0fc_32.jpg',
  },
  {
    id: 'U05PGHT8VF0',
    name: 'elliotfklein',
    profile_pic:
      'https://avatars.slack-edge.com/2023-08-26/5805151951139_341d57d53e65f00dc362_32.jpg',
  },
  {
    id: 'U05PLBZ0NMT',
    name: 'perfy',
    profile_pic:
      'https://secure.gravatar.com/avatar/3f03549709b0b8c32c1d6edc90e5c0db.jpg?s=32&d=https%3A%2F%2Fa.slack-edge.com%2Fdf10d%2Fimg%2Favatars%2Fava_0007-32.png',
  },
  {
    id: 'U05PP7C99PU',
    name: 'advait.maybhate9',
    profile_pic:
      'https://avatars.slack-edge.com/2023-08-26/5805154815971_3eb134f902f4f4c4e1fd_32.jpg',
  },
  {
    id: 'U05PRUP0Y68',
    name: 'advait',
    profile_pic:
      'https://avatars.slack-edge.com/2023-08-26/5807978041172_7cdf473ed1827aa92272_32.jpg',
  },
  {
    id: 'U05Q25AD9QR',
    name: 'advait429',
    profile_pic:
      'https://avatars.slack-edge.com/2023-08-26/5818184355121_84db3b6e7267485a65fc_32.jpg',
  },
  {
    id: 'U05Q29693RP',
    name: 'john_miller',
    profile_pic:
      'https://secure.gravatar.com/avatar/6412a7e41dc8b69a1999867f3a4c7ef2.jpg?s=32&d=https%3A%2F%2Fa.slack-edge.com%2Fdf10d%2Fimg%2Favatars%2Fava_0021-32.png',
  },
  {
    id: 'U05QCU28RQQ',
    name: 'acwangpython',
    profile_pic:
      'https://avatars.slack-edge.com/2023-08-26/5807762763780_de8209837dfd14fc41aa_32.png',
  },
];

const SOURCES = [
  {
    query: 'Bob recognizes other colleagues',
    threads: [
      {
        summarized:
          'Bob and Advait debug an issue causing the checkout page to crash and Bob thanks Advait for his help in resolution.',
        thread_id: '1693088817211029',
        thread_link:
          'https://performanceaigroup.slack.com/archives/C05PGS91WNS/p1693088817211029',
      },
      {
        summarized:
          'Bob gives kudos to his marketing colleague for a fantastic campaign',
        thread_id: '1693090307855649',
        thread_link:
          'https://performanceaigroup.slack.com/archives/C05PGS91WNS/p1693090307855649',
      },
      {
        summarized:
          'Bob commends the work on the frontend UI done by an engineer.',
        thread_id: '1693079791180469',
        thread_link:
          'https://performanceaigroup.slack.com/archives/C05PGS91WNS/p1693079791180469',
      },
    ],
  },
  // {
  //   query: 'Advait cares about what is best for the company',
  //   threads: [
  //     {
  //       summarized:
  //         'Advait pushes back against a fake demo to prop up sales, saying that it goes against their values.',
  //       thread_id: '1693089016455669',
  //       thread_link:
  //         'https://performanceaigroup.slack.com/archives/C05PGS91WNS/p1693089016455669',
  //     },
  //     {
  //       summarized:
  //         'Advait helps improve the onboarding process for engineers by suggesting a new idea.',
  //       thread_id: '1693079827092389',
  //       thread_link:
  //         'https://performanceaigroup.slack.com/archives/C05PGS91WNS/p1693079827092389',
  //     },
  //     {
  //       summarized:
  //         'Advait takes the time to explain a complicated concept to a junior engineer, walking through it step by step.',
  //       thread_id: '1693088646583389',
  //       thread_link:
  //         'https://performanceaigroup.slack.com/archives/C05PGS91WNS/p1693088646583389',
  //     },
  //   ],
  // },
  // {
  //   query: 'Lisa is very organized.',
  //   threads: [
  //     {
  //       summarized:
  //         'Lisa does a great job of leading meetings and summarizes the meeting afterwards, with takeaways',
  //       thread_id: '1693080406262219',
  //       thread_link:
  //         'https://performanceaigroup.slack.com/archives/C05PGS91WNS/p1693080406262219',
  //     },
  //     {
  //       summarized:
  //         'Lisa proactively brings up a feature that might be delayed so they can tackle it ahead of time.',
  //       thread_id: '1693091110054049',
  //       thread_link:
  //         'https://performanceaigroup.slack.com/archives/C05PGS91WNS/p1693091110054049',
  //     },
  //     {
  //       summarized:
  //         'Lisa approaches a design feasibility discussion in a thoughtful, organized manner interacting with the engineer in a great way.',
  //       thread_id: '1693082484621449g',
  //       thread_link:
  //         'https://performanceaigroup.slack.com/archives/C05PGS91WNS/p1693082484621449g',
  //     },
  //   ],
  // },
];

export const DEFAULT_SOURCE_MAP: SourcesMap = {
  U05Q25AD9QR: SOURCES,
  USLACKBOT: SOURCES,
  U05P8LXRC9M: SOURCES,
  U05PGHT8VF0: SOURCES,
  U05PLBZ0NMT: SOURCES,
  U05PP7C99PU: SOURCES,
  U05PRUP0Y68: SOURCES,
  U05Q29693RP: SOURCES,
  U05QCU28RQQ: SOURCES,
};
