<template>
  <div class="main">
    <el-container>
      <el-aside class="aside">
        <el-menu active-text-color="#ffd04b" background-color="#444444" default-active="1" text-color="#fff"
                 style="height:100%; width: 100%; overflow: hidden" :router="true">
          <div style="color: white; background-color: #181818;
          width: 100%; height: 10vh; display: flex; align-items: center; justify-content: center;">
            外汇-操作员
          </div>
  
          <el-menu-item :index="'/FExchange/operator?foreign_exchange_operator_id='+this.foreign_exchange_operator_id">
            <el-icon>
              <Avatar />
            </el-icon>
            <span>外币列表</span>
          </el-menu-item>
          <el-menu-item :index="'/FExchange/operator/addcurrency?foreign_exchange_operator_id='+this.foreign_exchange_operator_id">
            <el-icon>
              <Avatar />
            </el-icon>
            <span>新增外币</span>
          </el-menu-item>
          <div style="height: 30px"></div>
          <a href="/" style="margin-left: 40px;">
            <el-button type="danger">
              退出
            </el-button>
          </a>
        </el-menu>
      </el-aside>
      <el-container>
        <el-header style="height: 0vh;"></el-header>
        <el-main style="height: 100%; width: 100%; ">
          <el-scrollbar height="100%">
            <RouterView class="content" style="height: 95vh; max-height: 100%; background-color: white; color: black;" />
          </el-scrollbar>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
export default {
  data () {
    return {
      foreign_exchange_operator_id: 1
    }
  },
  created() {
    this.fetchDataFromUrl();
  },
  methods: {
    fetchDataFromUrl() {
      // 获取当前URL
      const url = new URL(window.location);
      // 创建URLSearchParams对象
      const params = new URLSearchParams(url.search);
      // 从查询字符串中获取参数
      this.foreign_exchange_operator_id = params.get('foreign_exchange_operator_id');
    },
    LogOut() {
      this.$router.push('/another-page');
    }
  }
}
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
  