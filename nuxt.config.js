const parseArgs = require("minimist")
const argv = parseArgs(process.argv.slice(2), {
  alias: {
    H: "hostname",
    p: "port"
  },
  string: ["H"],
  unknown: parameter => false
})

const port =
  argv.port ||
  process.env.PORT ||
  process.env.npm_package_config_nuxt_port ||
  "3000"
const host =
  argv.hostname ||
  process.env.HOST ||
  process.env.npm_package_config_nuxt_host ||
  "localhost"

// 追加.
const basePath = process.env.DEPLOY_ENV === 'GH_PAGES' ? '/nuxt-ts-plain/' : '/'
const routerBase = process.env.DEPLOY_ENV === 'GH_PAGES' ? {
  router: {
    base: basePath
  }
} : {}
const generateFolder = process.env.DEPLOY_ENV === 'GH_PAGES' ? 'docs' : 'dist'
module.exports = {
  // 追加.
  mode: 'spa',
  ...routerBase,
  env: {
    baseUrl:
      process.env.BASE_URL ||
      `http://${host}:${port}`
  },
  head: {
    title: "Azure LUIS demo",
    meta: [
      { charset: "utf-8" },
      {
        name: "viewport",
        content:
          "width=device-width, initial-scale=1"
      },
      {
        hid: "description",
        name: "description",
        content: "Nuxt.js project"
      }
    ],
    link: [
      {
        rel: "icon",
        type: "image/x-icon",
        href: "/favicon.ico"
      }
    ]
  },
  /*
  ** Customize the progress-bar color
  */
  loading: { color: "#3B8070" },
  // 追加.
  plugins: [
    { src: '~/plugins/chat.ts', ssr: false}
  ],
  vendor: ['vue-beautiful-chat'],
  generate: {
    dir: generateFolder
  },
  /*
  ** Build configuration
  */
  css: ["~/assets/css/main.css"],
  build: {},
  modules: [
    "@nuxtjs/axios",
    '@nuxtjs/dotenv',
    "~/modules/typescript.js"
  ],
  axios: {}
}
