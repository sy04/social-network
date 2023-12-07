<template>
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
    <div class="main-left col-span-1">
      <div class="p-4 bg-white border border-gray-200 text-center rounded-lg">
        <img :src="user.get_avatar" class="mb-6 rounded-full">
        <p><strong>{{ user.name }}</strong></p>

        <div class="mt-6 flex space-x-8 justify-around" v-if="user.id">
          <RouterLink :to="{name: 'friends', params: {id: user.id}}" class="text-xs text-gray-500">{{ user.friends_count }} friends</RouterLink>
          <p class="text-xs text-gray-500">{{ user.posts_count }} posts</p>
        </div>

        <div class="mt-6">
          <button
            class="inline-block py-5 px-3 bg-purple-600 text-xs text-white rounded-lg"
            @click="sendFriendshipRequest"
            v-if="userStore.user.id !== user.id"
          >
            Send Friendship Request
          </button>

          <button
            class="inline-block mt-4 py-5 px-3 bg-purple-600 text-xs text-white rounded-lg"
            @click="sendDirectMessage"
            v-if="userStore.user.id !== user.id"
          >
            Send Direct Message
          </button>

          <RouterLink
            class="inline-block mr-2 py-5 px-3 bg-purple-600 text-xs text-white rounded-lg"
            :to="{name: 'editprofile'}"
            v-if="userStore.user.id === user.id"
          >
            Edit Profile
          </RouterLink>

          <button
            class="inline-block py-5 px-3 bg-red-600 text-xs text-white rounded-lg"
            @click="logout"
            v-if="userStore.user.id === user.id"
          >
            Logout
          </button>
        </div>
      </div>
    </div>

    <div class="main-center col-span-2 space-y-4">
      <div
        class="bg-white border border-gray-200 rounded-lg"
        v-if="userStore.user.id === user.id"
      >
        <form v-on:submit.prevent="submitForm" method="post">
          <div class="p-4">  
            <textarea v-model="body" class="p-4 w-full bg-gray-100 rounded-lg" placeholder="What are you thinking about?"></textarea>
          </div>
  
          <div class="p-4 border-t border-gray-100 flex justify-between">
            <a href="#" class="inline-block py-4 px-6 bg-gray-600 text-white rounded-lg">Attach image</a>
            <button class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">Post</button>
          </div>
        </form>
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
  import { useUserStore } from '@/stores/user'
  import { useToastStore } from '@/stores/toast'
import { RouterLink } from 'vue-router';

  export default {
    name: 'ProfileView',
    setup() {
      const userStore = useUserStore()
      const toastStore = useToastStore()

      return {
        userStore,
        toastStore
      }
    },
    components: {
    PeopleYouMayKnow,
    Trends,
    FeedItem,
    RouterLink
},
    data() {
      return {
        posts: [],
        user: {
          id: ''
        },
        body: ''
      }
    },
    mounted() {
      this.getFeed()
    },
    watch: {
      "$route.params.id": {
        handler() {
          this.getFeed()
        },
        deep: true,
        immediate: true
      }
    },
    methods: {
      sendDirectMessage() {
        axios
          .get(`/api/chat/${this.$route.params.id}/get-or-create/`)
          .then((res) => {
            this.$router.push('/chat')
          })
          .catch((err) => {
            console.log('error', error)
          })
      },
      sendFriendshipRequest() {
        axios
          .post(`/api/friends/${this.$route.params.id}/request/`)
          .then((res) => {
            console.log('data', res.data)
            if(res.data.message === 'request already sent') {
                this.toastStore.showToast(5000, 'The request has already been sent!', 'bg-red-300')
            } else {
                this.toastStore.showToast(5000, 'The request sent!', 'bg-emerald-300')
            }
          })
          .catch((err) => {
            console.log('error', err.message)
          })
      },
      getFeed() {
        axios
          .get(`/api/posts/profile/${this.$route.params.id}/`)
          .then((res) => {
            this.posts = res.data.posts
            this.user = res.data.user
          })
          .catch((err) => {
            console.log('error', err.message)
          })
      },
      submitForm() {
        axios
          .post('/api/posts/create/', {
            'body': this.body
          })
          .then((res) => {
            console.log('data', res.data)

            this.posts.unshift(res.data)
            this.body = ''
            this.user.posts_count += 1
          })
          .catch((err) => {
            console.log('error', err)
          })
      },
      logout() {
        this.userStore.removeToken()
        this.$router.push('/login')
      }
    }
  }
</script>