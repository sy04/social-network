<template>
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
    <div class="main-center col-span-3 space-y-4">
      <div class="bg-white border border-gray-200 rounded-lg">
        <FeedForm
          v-bind:user=null
          v-bind:posts="posts"
        />
      </div>

      <div
        class="p-4 bg-white border border-gray-200 rounded-lg"
        v-for="(post, index) in posts"
        v-bind="index"
      >
        <FeedItem v-bind:post="post" />
      </div>
    </div>

    <div class="main-right col-span-1 space-y-4">
      <PeopleYouMayKnow />
      <Trends />
    </div>
  </div>
</template>

<script>
  import axios from 'axios'
  import PeopleYouMayKnow from '../components/PeopleYouMayKnow.vue';
  import Trends from '../components/Trends.vue';
  import FeedItem from '../components/FeedItem.vue';
  import FeedForm from '../components/FeedForm.vue';

  export default {
    name: 'FeedView',
    components: {
      PeopleYouMayKnow,
      Trends,
      FeedItem,
      FeedForm
    },
    data() {
      return {
        posts: [],
        body: ''
      }
    },
    mounted() {
      this.getFeed()
    },
    methods: {
      getFeed() {
        axios
          .get('/api/posts/')
          .then((res) => {
            this.posts = res.data
          })
          .catch((err) => {
            console.log('error', err.message)
          })
      },
      submitForm() {
        console.log('submitForm', this.body)

        axios
          .post('/api/posts/create/', {
            'body': this.body
          })
          .then((res) => {
            console.log('data', res.data)

            this.posts.unshift(res.data)
            this.body = ''
          })
          .catch((err) => {
            console.log('error', err)
          })
      }
    }
  }
</script>