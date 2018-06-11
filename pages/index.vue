<template>
  <section>
    <h1 class="header">{{ title }}</h1>
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
  luisApi:string = 'https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/0623e68e-1895-4e7e-91fb-baaa6ac546e0?subscription-key=1316ccc2a86b4066adcd78f0900a7bd1&verbose=true&timezoneOffset=0&q='


  // ■ Method.
  created () {
    console.log('created before DOM')
  }
  mounted () {
    console.log('mounted after DOM')
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
    let answer = '理解できませんでした'
    console.log('result', result)
    if ('topScoringIntent' in result) {
        let info = result.topScoringIntent
        if ( info.score >= 0.1 ) {
            if (info.intent === 'TestDrive') {
                answer = "試乗できる車は" + "\n" +
                    "・エスティマ" +　"\n" +
                    "・カローラ" +　"\n" +
                    "・タント" +　"\n" +
                    "です"
            } else if (info.intent === 'WantEstimate') {
                answer = "お見積りは1億円です。"
            } else if (info.intent === 'UseMonitor') {
                answer = "モニターのお問い合わせはこちらです。\n電話番号: XXXX-XXXX-XXXX"
            } else if (info.intent === 'CheckCarStatus') {
                answer = "調子の良い車は エスティマ です"
            } else if (info.intent === 'PayKnow') {
                answer = "お支払額は以下のとおりです。" + "\n" +
                    "・エスティマ: 400万円" +　"\n" +
                    "・カローラ: 380万円" +　"\n" +
                    "・タント: 100万円" +　"\n"
            } else if (info.intent === 'Redmine') {
                answer = "社内ルールが書かれたURLを教えるね。" + "\n" + 
                    "http://redmine3.genio.co.jp/projects/geniocom/wiki" 
            } else {
                answer = "理解できませんでした。"
            }
        } else {
            answer = "その質問は学習されていません。LUISを賢くしてください。"
        }
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