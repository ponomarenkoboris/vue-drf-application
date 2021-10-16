<script setup lang="ts">
import { useRoute } from 'vue-router'
import 'vfonts/FiraCode.css'

const route = useRoute()

</script>

<template>
	<n-page-header v-if="route.path !== '/auth'" class="page__header">
		<template #header>
			<n-space justify="space-between">
				<n-breadcrumb>
					<n-breadcrumb-item>
						<router-link to="/tasks" active-class="active_route" class="route">Task List</router-link>
					</n-breadcrumb-item>
					<n-breadcrumb-item>
						<router-link to="/chat" active-class="active_route" class="route">Chat</router-link>
					</n-breadcrumb-item>
					<n-breadcrumb-item>
						<router-link to="/text-editor" active-class="active_route" class="route">Text Editor</router-link>
					</n-breadcrumb-item>
					<n-breadcrumb-item>
						<router-link to="/settings" active-class="active_route" class="route">Settings</router-link>
					</n-breadcrumb-item>
				</n-breadcrumb>
			</n-space>
		</template>
	</n-page-header>
</template>
<style lang="scss" scoped>
.page__header {
	padding-top: 30px;
	margin: 0 100px;
	.route {
		text-decoration: none;
		color: initial;
		font-size: larger;
	}

	.active_route {
		color: #63e2b7;
	}
}

.layout {
	padding-top: 30px;
	height: 100vh;
	width: 100vw;
}
</style>