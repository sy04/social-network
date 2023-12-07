<template>
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
    <div class="main-center col-span-3 space-y-4">
      <div
        class="p-4 bg-white border border-gray-200 rounded-lg"
        v-for="notification in notifications"
        v-bind:key="notification.id"
        v-if="notifications.length"
      >
        {{ notification.body }}

        <button class="underline" @click="readNotification(notification)">Read more</button>
      </div>
      <div
        class="p-4 bg-white border border-gray-200 rounded-lg"
        v-else
      >
        You dont have any unread notifications!
      </div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios';

  export default {
    name: 'notifications',
    data() {
      return {
        notifications: []
      }
    },
    mounted() {
      this.getNotifications()
    },
    methods: {
      getNotifications() {
        axios
          .get('/api/notifications/')
          .then((res) => {
            this.notifications = res.data
          })
          .catch((err) => {
            console.log('error', err)
          })
      },
      async readNotification(notification) {
        await axios
          .post(`/api/notifications/read/${notification.id}/`)
          .then((res) => {
            if(
              notification.type_of_notification == 'post_like' ||
              notification.type_of_notification == 'post_comment'
            ) {
              this.$router.push({name: 'postview', params: {id: notification.post_id}})
            } else {
              this.$router.push({name: 'friends', params: {id: notification.created_for_id}})
            }
          })
          .catch((err) => {
            console.log('error', err)
          })
      }
    }
  }

</script>