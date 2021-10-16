<script lang="ts" setup>
import { ref, computed } from 'vue'
import marked from 'marked'

const fileName = ref<string>('')
const markdown = ref<string>('')
const textRef = ref<HTMLDivElement>()
const changeFileName = ref<boolean>(false)
const mardownToHTML = computed(() => marked(markdown.value))

</script>

<template>
    <n-layout style="height: 90vh;">
        <n-layout-header
            style="height: 50px;"
            bordered
        >
            <n-space justify="center">
                <n-h2 v-if="!changeFileName" @click="() => changeFileName = true">{{ fileName }}</n-h2>
                <div v-else>
                    <n-input v-model:value="fileName" />
                    <n-button @click="() => changeFileName = false"></n-button>
                </div>              
            </n-space>
        </n-layout-header>
        <n-layout position="absolute" style="top: 40px; bottom: 64px;" has-sider>
            <n-layout-sider
                content-style="padding: 24px;"
                :native-scrollbar="false"
                bordered
            >
                <n-h3 v-for="n in 20" :key="n">{{ n }}</n-h3>
            </n-layout-sider>
            <n-layout 
                content-style="padding: 24px;" 
                :native-scrollbar="false"
                
            >
                <div class="main_layout">
                    <textarea 
                        id="textarea"
                        v-model="markdown"
                    ></textarea>
                    <div ref="textRef" v-html="mardownToHTML" class="page"></div>
                </div>
            </n-layout>
        </n-layout>
        <n-layout-footer
            position="absolute"
            style="height: 64px; padding: 24px;"
            bordered
        >
            <n-space justify="center">
                <n-h2>Footer</n-h2>
            </n-space>
        </n-layout-footer>
    </n-layout>
</template>
<style lang="scss" setup>
.main_layout {
    width: 100%;
    height: 100%;
    display: flex;

    #textarea {
        resize: none;
        height: 700px;
        width: 30%;
        outline: none;
        border: none;
        border-right: 1px solid #e9e9e9;
        background-color: #e9e9e9;
        padding: 5px 10px;
        font-size: 17px;
    }

    .page {
        margin-left: 10px;
        width: 70%;
    }
}
</style>