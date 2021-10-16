<script lang="ts" setup>
// TODO append password changing logic and debug (rooms are missing when username is changed)
import setCSRFHeader, { request, endpoints } from '../utils'
import { UserAvatar, Pen } from '@vicons/carbon'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { reactive, ref } from 'vue'
import formRules, { validatePasswordSame } from '../validators'

type TProfile = {
    [index: string]: string,
    username: string,
    firstName: string,
    lastName: string,
    avatarImage: string,
    password: string
}

const userProfile = reactive<TProfile>({
    username: '',
    firstName: '',
    lastName: '',
    avatarImage: '',
    password: '',
})
const newUserData = reactive<TProfile>({
    username: '',
    firstName: '',
    lastName: '',
    avatarImage: '',
    password: '',
    rePassword: ''
})
const store = useStore()
const router = useRouter()
const formRef = ref<HTMLFormElement>()

const rules = {
    ...formRules,
    rePassword: {
        trigger: 'input',
        validator: validatePasswordSame(newUserData)
    }
}

request.get(endpoints.userInfo)
    .then(response => {
        if (response.data.user && response.data.username ) {
            const { last_name: lastName, first_name: firstName, id, avatar_image: avatarImage } = response.data.user
            userProfile.firstName = firstName
            userProfile.lastName = lastName
            userProfile.username = response.data.username
            userProfile.avatarImage = avatarImage
        }
    })
    .catch(error => {
        console.log(error)
    })

const logout = async (): Promise<void> => {
	try {
		const response = await request.post(endpoints.logout, {}, { headers: {...setCSRFHeader()} })
		if (response.data.success) {
            localStorage.clear()
			router.replace('/auth')
			store.commit('clearStore')
		}
	} catch (error) {
        console.error(error)
	}
}

const beforeUpload = async ({ file }: { file: any }): Promise<boolean> => {
    if (file.file.type === 'image/png' || file.file.type === 'image/jpeg' || file.file.type === 'image/jpg') {
        const reader = new FileReader()
        reader.onload = (ev:  ProgressEvent<FileReader>): void => {
            userProfile.avatarImage = ev.target?.result as string
            newUserData.avatarImage = ev.target?.result as string
        }
        reader.readAsDataURL(file.file)

        return true
    }
    return false
}

const submitProfileChanges = async (e: MouseEvent): Promise<boolean | void> => {
    e.preventDefault()
    formRef.value?.validate(async (errors: any): Promise<void | boolean> => {
        if (!errors) {
            try {
                const payload = Object.assign({}, newUserData)
                for (let key in payload) {
                    if (key === 'username' && payload[key].trim()) localStorage.setItem('username', payload[key])
                    if (!payload[key].trim() || key === 'rePassword') delete payload[key]
                }
                const response = await request.put(endpoints.updateAccount, payload, { headers: { ...setCSRFHeader() } })
                if (response.data.succes) {
                    for (let key in payload) {
                        userProfile[key] = payload[key]
                        newUserData[key] = ''
                    }
                    if (newUserData.rePassword) newUserData.rePassword = ''
                }
            } catch (error) {
                console.error(error)
            }      
        }  
        else return false
    })
}

</script>
<template>
    <div 
        v-if="!userProfile.username"
        class="spin_wrapper"
    >
        <n-spin size="large" />
    </div>
    <n-space v-else
        justify="center"
    >
        <n-space vertical>
            <n-button 
                class="logout_btn"
                block
                type="error" 
                @click="logout"
            >
                Logout
            </n-button>
            <div class="icon_wrapper">
                <n-icon v-if="!userProfile.avatarImage"  size="200">
                    <UserAvatar />
                </n-icon>
                <img v-else :src="userProfile.avatarImage" alt="User avatar" class="avatar_image">
            </div>
            <n-form
                ref="formRef"
                :model="newUserData"
                class="user_info"
                :rules="rules"
            >
                <n-form-item 
                    path="avatarImage"
                    class="upload_btn_wrapper"
                >
                    <n-upload
                        @before-upload="beforeUpload"
                        @remove="() => newUserData.avatarImage = ''"
                    >
                        <n-button>Upload Avatar</n-button>
                    </n-upload>
                </n-form-item>

                <n-collapse class="collapse_wrapper">
                    <template #header-extra>
                        <n-icon size="17">
                            <Pen/>
                        </n-icon>
                    </template>
                    <n-collapse-item 
                        :title="`Username: ${userProfile.username}`"
                        class="collapse_item"
                    >
                        <n-form-item path="username">
                            <n-input 
                                placeholder="Enter username"
                                v-model:value="newUserData.username"
                            />
                        </n-form-item>
                    </n-collapse-item>
                    <n-collapse-item 
                        :title="`First name: ${userProfile.firstName}`"
                        class="collapse_item"
                    >
                        <n-form-item path="firstName">
                            <n-input 
                                placeholder="Enter first name"
                                v-model:value="newUserData.firstName"
                            />
                        </n-form-item>
                    </n-collapse-item>
                    <n-collapse-item 
                        :title="`Last name: ${userProfile.lastName}`"
                        class="collapse_item"
                    >
                        <n-form-item path="lastName">
                            <n-input 
                                placeholder="Enter last name"
                                v-model:value="newUserData.lastName"
                            />
                        </n-form-item>
                    </n-collapse-item>
                    <n-collapse-item 
                        :title="`Change password`"
                        class="collapse_item"
                    >
                        <n-form-item path="password">
                            <n-input 
                                type="password"
                                placeholder="Enter new password"
                                v-model:value="newUserData.password"
                                show-password-on="mousedown"
                            />
                        </n-form-item>
                        <n-form-item path="rePassword">
                            <n-input 
                                type="password"
                                placeholder="Enter re-password"
                                v-model:value="newUserData.rePassword"
                                show-password-on="mousedown"
                            />
                        </n-form-item>
                    </n-collapse-item>
                </n-collapse>
                <n-button 
                    class="submit_btn"
                    type="primary" 
                    @click="submitProfileChanges"
                    block
                >
                    Submit changes
                </n-button>
            </n-form>
        </n-space>
    </n-space>
</template>

<style lang="scss" setup>
.spin_wrapper {
    display: flex;
    justify-content: space-around;
}
.logout_btn {
    margin-bottom: 10px;
}

.icon_wrapper {
    display: flex;
    justify-content: center;

    .avatar_image {
        width: 175px;
        height: 175px;
        border-radius: 50%;
        object-fit: cover;
    }
}
.user_info {
    width: 500px;

    .collapse_wrapper {
        margin: 20px 0 30px;
    }
    
    .upload_btn_wrapper {
        display: flex;
        justify-content: center;
    }

    .submit_btn {
        margin-top: 5px;
    }
}
</style>