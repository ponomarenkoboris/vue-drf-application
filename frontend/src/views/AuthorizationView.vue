<script lang="ts" setup>
import { reactive, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import formRules, { validatePasswordSame } from '../validators'
import getCSRFHeader, { request, endpoints } from '../utils'

type TLoginData = {
	username: string,
	password: string
}

type TRegisterData = {
	username: string,
	firstName: string,
	lastName: string,
	password: string,
	rePassword: string
}

const router = useRouter()
const isLogin = ref<boolean>(true)
const registerFormRef = ref<HTMLFormElement>()
const registerData = reactive<TRegisterData>({
	username: '',
	firstName: '',
	lastName: '',
	password: '',
	rePassword: ''
})
const loginData = reactive<TLoginData>({
	username: '',
	password: ''
})

const errorCreated = ref<boolean>(false)
const errorMessage = ref<string>("I'm back in the U.S.S.R.")

const rules = {
    ...formRules,
    rePassword: {
        trigger: 'input',
        validator: validatePasswordSame(registerData)
    }
}

watch(isLogin, (_, prev) => {
	if (prev) {
		loginData.username = ''
		loginData.password = ''
	}
	if (!prev) {
		registerData.username = ''
		registerData.firstName = ''
		registerData.lastName = ''
		registerData.password = ''
		registerData.rePassword = ''
	}
})

const login = async (): Promise<void> => {
	try {
		const response = await request.post(endpoints.login, loginData, { headers: { ...getCSRFHeader() } })
		if (response.data.success) {
			localStorage.setItem('username', loginData.username)
			router.push('/tasks')
		} else {
			throw new Error('error')
		}

	} catch (error) {
		errorMessage.value = 'Something went wrong while trying to create user.'
		errorCreated.value = true
	}
}

const registration = async (): Promise<void> => {
	const { password, rePassword } = registerData

	if (password.trim().length < 6 || rePassword.trim().length < 6 || password !== rePassword) {
		errorMessage.value = 'Password did not match.'
		errorCreated.value = true
		return
	}
	
	try {
		const response = await request.post(endpoints.registaration, registerData, { headers: { ...getCSRFHeader() } })
		if (response.data.success) {
			localStorage.setItem('username', registerData.username)
			router.push('/tasks')
		} else {
			throw new Error('error')
		}
	} catch (error) {
		errorMessage.value = (error as Error)?.message ? (error as Error).message : 'Something went wrong while trying to create user.'
		errorCreated.value = true
	}
}

</script>
<template>
	<div class="auth_wrapper">
		<n-card id="auth_card">
			<n-tabs default-value="signin" size="large">
				<n-tab-pane name="signin" tab="Sign in">
					<n-form>
						<n-form-item-row label="Username">
							<n-input
								id="input_field"
								type="text" 
								placeholder="Username" 							
								autocomplete="username"
								v-model:value="loginData.username"
							/>
						</n-form-item-row>
						<n-form-item-row label="Password">
							<n-input 
								type="password"
								show-password-on="mousedown"
								placeholder="Password"
								autocomplete="current-password"
								v-model:value="loginData.password"
							/>
						</n-form-item-row>
					</n-form>
					<n-button type="primary" block ghost @click="login">Sign In</n-button>
				</n-tab-pane>
				<n-tab-pane name="signup" tab="Sign Up">
					<n-form
						ref="registerFormRef"
						:model="registerData"
						:rules="rules"
					>
						<n-form-item-row label="First name" path="firstName">
							<n-input 
								type="text"
								id="input_field"
								placeholder="Firts name"							
								v-model:value="registerData.firstName"
							/>
						</n-form-item-row>
						<n-form-item-row label="Last name" path="lastName">
							<n-input 
								type="text" 
								placeholder="Last name"							
								v-model:value="registerData.lastName"
							/>
						</n-form-item-row>
						<n-form-item-row label="Username" path="username">
							<n-input 
								type="text" 
								placeholder="Enter username"							
								autocomplete="username"
								v-model:value="registerData.username"
							/>
						</n-form-item-row>
						<n-form-item-row label="Password" path="password">
							<n-input 
								type="password" 
								placeholder="Password" 							
								show-password-on="mousedown"
								v-model:value="registerData.password"
							/>
						</n-form-item-row>
						<n-form-item-row label="Reenter Password" path="rePassword">
							<n-input 
								type="password" 
								placeholder="Password"
								show-password-on="mousedown"
								v-model:value="registerData.rePassword"
							/>
						</n-form-item-row>
					</n-form>
					<n-button type="primary" block ghost @click="registration">Sign Up</n-button>
				</n-tab-pane>
			</n-tabs>
		</n-card>
		<n-alert 
			v-if="errorCreated" 
			title="Error Text" 
			type="error" 
			closable
			@close="() => errorCreated = false"
		>
			{{ errorMessage }}
		</n-alert>
	</div>
</template>

<style lang="scss" scoped>
.auth_wrapper {
	height: 100vh;
	width: 100vw;
	display: flex;
	align-items: center;
	justify-content: center;

	#auth_card {
		max-width: 398px;

		#input_field {
			min-width: 300px;
		}
	}
}
</style>