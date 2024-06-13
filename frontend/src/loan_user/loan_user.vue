<template>
  <div class="main">
    <el-container>
      <el-aside class="aside">
        <el-menu active-text-color="#ffd04b" background-color="#444444" default-active="1" text-color="#fff"
                 style="height:100%; width: 100%; overflow: hidden" :router="true">
          <div style="color: white; background-color: #181818;
          width: 100%; height: 10vh; display: flex; align-items: center; justify-content: center;">
            用户操作界面  {{user_id}}
          </div>
          <!-- 通过url参数形式传递给子组件 -->
          <el-menu-item :index=" '/loan_user/loan?user_id=' + this.user_id">
            <el-icon>
              <Avatar />
            </el-icon>
            <span>申请贷款</span>
          </el-menu-item>
          <el-menu-item :index=" '/loan_user/withdrawal?user_id=' + this.user_id">
            <el-icon>
              <Avatar />
            </el-icon>
            <span>申请还款</span>
          </el-menu-item>
          <el-menu-item :index=" '/loan_user/query?user_id=' + this.user_id">
            <el-icon>
              <Avatar />
            </el-icon>
            <span>查询记录</span>
          </el-menu-item>
          <div style="height: 30px"></div>
          <a href="/login" style="margin-left: 40px;">
            <el-button type="danger">
              退出
            </el-button>
          </a>
        </el-menu>

      </el-aside>
      <el-container>
        <el-main style="height: 100%; width: 100%; ">
          <el-scrollbar height="100%">
            <RouterView class="content" style="height: 100vh; max-height: 100%; background-color: white; color: black;" />
          </el-scrollbar>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import {Avatar} from "@element-plus/icons-vue";

export default {
  components: {Avatar},
  created() {
    this.fetchDataFromUrl();
  },
  data(){
    return{
      user_id:0
    }
  },
  methods: {
    fetchDataFromUrl() {
      // 获取当前URL
      const url = new URL(window.location);
      // 创建URLSearchParams对象
      const params = new URLSearchParams(url.search);
      // 从查询字符串中获取参数
      this.user_id = params.get('user_id');
    }
  }
};
</script>

<style scoped>
#app {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  background-color: #dcdcdc;
  width: 100vw;
  height: 100vh;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  width: 100%;
  min-height: 100%;
  height: auto;
  background-color: #dcdcdc;

}

.title {
  background-color: #ffffff;
  height: 60px;
}

.aside {
  min-height: 100vh;
  width: 200px;
  background-color: black;
}
</style>
