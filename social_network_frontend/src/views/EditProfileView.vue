<template>
  <div class="max-w-7xl mx-auto grid grid-cols-2 gap-4">
    <div class="main-left">
      <div class="p-12 bg-white border border-gray-200 rounded-lg">
        <h1 class="mb-6 text-2xl">Edit Profile</h1>

        <p class="mb-6 text-gray-500">
          Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate.
          Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate.
        </p>

        <RouterLink :to="{name: 'editpassword'}" class="underline">Edit Password</RouterLink>
      </div>
    </div>
    <div class="main-right">
      <div class="p-12 bg-white border border-gray-200 rounded-lg">
        <form class="space-y-6" v-on:submit.prevent="submitForm">
          <div>
            <label>Name</label><br>
            <input type="text" v-model="form.name" placeholder="Your fullname" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
          </div>

          <div>
            <label>E-mail</label><br>
            <input type="email" v-model="form.email" placeholder="Your e-mail address" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
          </div>

          <div>
            <label>Avatar</label><br>
            <input type="file" ref="file">
          </div>

          <template v-if="errors.length > 0">
            <div class="bg-red-300 text-white rounded-lg p-6">
              <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
            </div>
          </template>

          <div>
            <button class="py-4 px-6 bg-purple-600 text-white rounded-lg">Save Changes</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios'
  import { useToastStore } from '@/stores/toast'
  import { useUserStore } from '@/stores/user'
  import { RouterLink } from 'vue-router'

  export default {
    setup() {
      const toastStore = useToastStore();
      const userStrore = useUserStore();

      return {
        toastStore,
        userStrore
      };
    },
    data() {
      return {
        form: {
          email: this.userStrore.user.email,
          name: this.userStrore.user.name,
        },
        errors: []
      };
    },
    methods: {
        submitForm() {
            this.errors = [];

            if (!this.form.email) this.errors.push('Your email is missing');
            if (!this.form.name) this.errors.push('Your name is missing');

            if (this.errors.length === 0) {
              let formData = new FormData();
              formData.append('avatar', this.$refs.file.files[0]);
              formData.append('name', this.form.name);
              formData.append('email', this.form.email);
              axios
                .post('/api/editprofile/', formData, {
                  headers: {
                    "Content-Type": "multipart/form-data"
                  }
                })
                .then((res) => {
                  if (res.data.message === 'information updated') {
                    this.toastStore.showToast(5000, 'The information was saved', 'bg-emerald-500');
                    this.userStrore.setUserInfo({
                      id: this.userStrore.user.id,
                      name: this.form.name,
                      email: this.form.email,
                      avatar: res.data.user.get_avatar
                    });
                    this.$router.back();
                  }
                  else {
                    this.toastStore.showToast(5000, 'Something went wrong. Please try again', 'br-red-300');
                  }
                })
                .catch((err) => {
                  console.log(err);
                });
            }
        }
    },
    components: { RouterLink }
}
</script>