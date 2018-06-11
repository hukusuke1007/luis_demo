<template>
  <section>
    <h1 class="header">{{ title }}</h1> 
    <div>
      <h2>徳島県について聞いてみよう！</h2>
      (多分)理解できる質問集
      <ul>
        <li>徳島県について</li>
        <li>徳島県の行き方</li>
        <li>徳島県について</li>
        <li>かずら橋について</li>
        <li>小便小僧について</li>
      </ul>
    </div>
    <div>
      <button class="square_btn" @click="isChatOpen=true">チャットする！</button>
      <beautiful-chat
        :agentProfile="agentProfile"
        :onMessageWasSent="onMessageWasSent"
        :messageList="messageList"
        :newMessagesCount="newMessagesCount"
        :isOpen="isChatOpen"
        :close="closeChat"
        :open="openChat"
        :showEmoji="true"
        :showFile="true" />
    </div>
  </section>
</template>

<script lang="ts">
import {
  Component,
  Vue
} from "nuxt-property-decorator"
import axios from 'axios'

@Component({
  components: {
  }
})
export default class extends Vue {
  title: string = 'Azure LUIS demo'
  message: string = 'test'
  agentProfile: any = {
    teamName: this.title,
    imageUrl: 'https://a.slack-edge.com/66f9/img/avatars-teams/ava_0001-34.png'
  }
  messageList: Array<any> = []
  newMessagesCount:number = 0
  isChatOpen = false
  text: string = ""

  // ■ Luis API
  luisApi:any = process.env.LUIS_API

  // ■ Method.
  created () {
    console.log('created before DOM')
  }
  mounted () {
    console.log('mounted after DOM', process.env.LUIS_API)
  }
  sendMessage (msg: any) {
    console.log('sendMessage', msg)
    if (msg.data.text.length > 0) {
      this.newMessagesCount = this.isChatOpen ? this.newMessagesCount : this.newMessagesCount + 1
      this.messageList.push(msg)
    }
  }
  onMessageWasSent (msg) {
    console.log('onMessageWasSent', msg)

    // 自分のメッセージを表示.
    this.messageList.push(msg)
    
    // LUISよろしく.
    this.luisAnalyze(msg.data.text)
      .then((result) => {
        // LUISの結果を元に処理.
        this.luisResult(result)
      }).catch((error) => {
        console.error('error', error)
      })
  }
  openChat () {
    this.isChatOpen = true
    this.newMessagesCount = 0
  }
  closeChat () {
    this.isChatOpen = false
  }
  async luisAnalyze(msg: string): Promise<any> {
    let url:string = this.luisApi + "\"" + msg + "\""
    console.log('url', url)
    let answer = await axios.get(url)
    let result = answer.data
    return result
  }
  luisMessage (message: string) {
    let msg: any = {
      author: 'luis',
      type: 'text',
      data: {
        text: message
      }      
    }
    this.sendMessage(msg)
  }
  luisResult(result: any): void {
    let msg = ''
/*
{intent: "Tokushima", score: 0.433965236}
{intent: "HowToGetPlace", score: 0.137868986}
{intent: "Kazurabashi", score: 0.009012208}
{intent: "Shonbenkozou", score: 0.00691728434}
{intent: "None", score: 0.00683180755}
*/
    console.log('result', result)
    if ('topScoringIntent' in result) {
      let info:any= result.topScoringIntent
      // 認識率20%以上なら処理する(甘め)
      if ( info.score >= 0.2 ) {
          let url:string = 'https://www.google.co.jp/'
          if (info.intent === 'Tokushima') {
            msg = 'OK！徳島県の地図をだしたから見てね！'
            url = 'https://www.google.co.jp/maps/place/%E5%BE%B3%E5%B3%B6%E7%9C%8C/@34.1410563,133.7733708,8z/data=!4m5!3m4!1s0x35524d5baed737b3:0xfddd63f964cf310c!8m2!3d34.0657179!4d134.5593601'
          } else if (info.intent === 'HowToGetPlace') {
            msg = 'OK！徳島県の行き方のサイトを案内したから見てね！'
            url = 'https://www.awanavi.jp/access/'
          } else if (info.intent === 'Kazurabashi') {
            msg = 'OK！かずら橋の観光サイトを案内したから見てね！'
            url = 'http://miyoshinavi.jp/02miru/detail.php?genr=101&uid=SS000048'
          } else if (info.intent === 'Shonbenkozou') {
            msg = 'OK！小便小僧の観光サイトを案内したから見てね！'
            url = 'https://www.shikoku.gr.jp/spot/696'
          } else {
            msg = 'うーん....とりあえずGoogle開いたからそこから検索してね！'
          }
          window.open(url, '_blank')
      } else {
          msg = "ごめんなさい！質問が分からないんです。もっと徳島県について勉強します！"
      }
      this.luisMessage(msg)
    }
  }
}
</script>
<style scoped>
.header {
  font-family: "Segoe UI", Tahoma, Geneva, Verdana,
    sans-serif;
}
/* 追加 */
.square_btn{
    display: inline-block;
    padding: 0.5em 1em;
    text-decoration: none;
    background: #668ad8;
    color: #FFF;
    border-bottom: solid 4px #627295;
    border-radius: 3px;
}
.square_btn:active {
    -ms-transform: translateY(4px);
    -webkit-transform: translateY(4px);
    transform: translateY(4px);
    border-bottom: none;
}
</style>