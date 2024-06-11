<template>
    <el-scrollbar height="100%" style="width: 100%; height: 100%">
      <div style="margin-left:30px;font-size: 40px; margin-top: 20px; font-weight: bold">
        信用卡</div>
      <div style="margin-left:20px; display: flex;flex-wrap: wrap; justify-content: start;">
        <!-- 申请信用卡接口 -->
        <el-button class="creditcardBox" @click="newApplicationVisible = true">
          <el-icon style="height: 50px; width: 50px;">
            <Plus style="height: 100%; width: 100%;" />
          </el-icon>
        </el-button>

        <!-- 查看申请接口 -->
        <el-button class="creditcardBox"  @click="showApplyListVisible=true">
          <el-icon style="height: 50px; width: 50px;">
            <View style="height: 100%; width: 100%;" />
          </el-icon>
        </el-button>

        <!-- 信用卡信息显示卡片 -->
        <div class="creditcardBox" v-for="creditcard in creditcards" :key="creditcard.account_id">
          <div>
            <!-- 卡片标题 -->
            <div style="font-size: 25px; font-weight: bold;">No. {{creditcard.account_id}}</div>

            <el-divider />

            <!-- 卡片内容 -->
            <div style="margin-left: 10px; text-align: start; font-size: 16px;">
              <p style="padding: 2.5px;"><span style="font-weight: bold">余额：</span>{{creditcard.balance}}</p>
              <p style="padding: 2.5px;"><span style="font-weight: bold">信用额度：</span>{{creditcard.limit}}</p>
              <p style="padding: 2.5px;"><span style="font-weight: bold">开户日期：</span>{{creditcard.open_date}}</p>
              <p style="padding: 2.5px;">
                <el-tag v-if="creditcard.is_frozen">已冻结</el-tag>
                <el-tag v-if="creditcard.is_lost" style="margin-left: 10px">已挂失</el-tag>
                <el-tag v-if="!creditcard.is_frozen && !creditcard.is_lost">正常</el-tag>
              </p>
            </div>
            <el-divider />

            <!-- 卡片操作 -->
            <div style="margin-top: 10px; margin-left: 35px; display:flex; ">

              <!-- 冻结信用卡 -->
              <el-button @click="this.newFreezeCredit.account_id=creditcard.account_id,
                this.freezeCreditVisible=true" type="primary" circle>
                 <el-icon><Lock /></el-icon>
              </el-button>

              <!-- 挂失信用卡 -->
              <el-button  @click="this.newReportLoss.account_id=creditcard.account_id,
                this.ReportLoss = true" type="primary" circle >
                <el-icon><DocumentDelete /></el-icon>
              </el-button>

              <!-- 取消信用卡 -->
              <el-button @click="this.cancelCardInfo.account_id=creditcard.account_id,
                this.CancelCard=true" circle type="primary">
                <el-icon><Close /></el-icon>
              </el-button>

              <!-- 更新密码 -->
              <el-button @click="this.newPassword.account_id=creditcard.account_id,
                this.UpdatePassword=true" circle type="primary">
                <el-icon><Key /></el-icon>
              </el-button>
            </div>

            <div style="margin-top: 3px; margin-left: 35px; display:flex" >

              <!-- 更新额度 -->
              <el-button  @click="this.newUpdateLimit.account_id=creditcard.account_id,
                this.UpdateLimit=true" type="primary" circle>
                <el-icon><Coin /></el-icon>
              </el-button>

              <!-- 支付功能 -->
              <el-button @click="this.newPayBill.account_id=creditcard.account_id,
                this.PayBill=true"  type="primary" circle>
                <el-icon><ShoppingCart /></el-icon>
              </el-button>

              <!-- 信用卡还款 -->
              <el-button @click="this.newRepayCredit.account_id=creditcard.account_id,
                this.RepayCredit=true" type="primary" circle>
                <el-icon><CreditCard /></el-icon>
              </el-button>

              <!-- 查看月账单 -->
              <el-button  @click="this.billInfo.account_id=creditcard.account_id,
              this.ViewBill = true" type="primary" circle>
                <el-icon><List /></el-icon>
              </el-button>
            </div>
          </div>
        </div>
      </div>

      <!-- 申请信用卡对话框 -->
      <el-dialog v-model="newApplicationVisible" title="申请信用卡" width="30%" align-center>
      <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
          年收入：
          <el-input v-model="newApplicationInfo.annual_income" style="width: 12.5vw;" clearable />
         元
       </div>
        <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
          总资产：
          <el-input v-model="newApplicationInfo.property_valuation" style="width: 12.5vw;" clearable />
          元
        </div>
        <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
          总工龄：
          <el-input v-model="newApplicationInfo.service_year" style="width: 12.5vw;" clearable />
          年
        </div>

      <template #footer>
            <span>
                <el-button @click="this.newApplicationVisible = false">取消</el-button>
                <el-button type="primary" @click="ConfirmApply"
                  :disabled="newApplicationInfo.annual_income <= 0 ||
                  newApplicationInfo.property_valuation <= 0 ||
                  newApplicationInfo.service_year < 0  ">确定</el-button>
            </span>
        </template>
      </el-dialog>

      <!-- 查看申请 -->
      <el-dialog v-model="showApplyListVisible" title="查看信用卡申请记录" width="50%" align-center>
        <div style="display: flex; margin-bottom: 20px;">
          <div style="margin-left: 2vw; margin-top: 20px; text-align: center;">
            <el-button type="primary" @click="ConfirmShowApplyList">查询</el-button>
          </div>
          <div style="margin-left: 2vw; margin-top: 20px; text-align: center;">
            <el-button type="primary" @click="showList=false,showApplyListVisible=false">退出</el-button>
          </div>
        </div>
        <el-scrollbar height="100%" style="width: 100%; height: 100%">
          <div style="display: flex;">
            你的申请记录如下：
          </div>
          <el-table :data="applyList" v-if="showList" :table-layout="'auto'"
            :default-sort="{ prop: 'date', order: 'ascending' }"
            style="width: 100%; margin-left: 5px; margin-top: 30px; margin-right: 5px; max-width: 80vw;">
            <el-table-column prop="apply_id" label="申请单号" sortable />
            <el-table-column prop="apply_date" label="申请时间" />
            <el-table-column prop="examiner_id" label="审核员ID" sortable />
            <el-table-column prop="apply_status" label="审核状态">
              <template v-slot ="scope">{{ scope.row.apply_status ? '已审核' : '待审核' }}</template>
            </el-table-column>
            <el-table-column prop="apply_result" label="审核结果">
              <template v-slot ="scope">{{ scope.row.apply_result ? '通过' : '不通过' }}</template>
            </el-table-column>
            <el-table-column prop="have_open" label="开卡结果">
              <template v-slot ="scope">{{ scope.row.apply_result ? '已开卡' : '未开卡' }}</template>
            </el-table-column>
          </el-table>
        </el-scrollbar>
      </el-dialog>

      <!-- 冻结对话框 -->
      <el-dialog v-model="freezeCreditVisible" title="冻结信用卡" width="30%" align-center>
      <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
          密码：
          <el-input v-model="newFreezeCredit.password" style="width: 12.5vw;" clearable />
      </div>
      <template #footer>
          <span>
              <el-button @click="this.freezeCreditVisible = false">取消</el-button>
              <el-button type="primary" @click="ConfirmFreezeCredit"
                  :disabled="newFreezeCredit.password.length === 0">确定</el-button>
          </span>
      </template>
      </el-dialog>

      <!-- 挂失对话框 -->
      <el-dialog v-model="ReportLoss" title="挂失信用卡" width="30%" align-center>
        <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
            密码：
            <el-input v-model="newReportLoss.password" style="width: 12.5vw;" clearable />
        </div>

        <template #footer>
            <span>
                <el-button @click="this.ReportLoss = false">取消</el-button>
                <el-button type="primary" @click="ConfirmReportLoss"
                    :disabled="newReportLoss.password.length === 0">确定</el-button>
            </span>
        </template>
        </el-dialog>

      <!-- 取消对话框 -->
      <el-dialog v-model="CancelCard" title="取消信用卡" width="30%" align-center>
        <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
            输入密码：
            <el-input v-model="cancelCardInfo.password" style="width: 12.5vw;" clearable />
        </div>

        <template #footer>
            <span>
                <el-button @click="this.CancelCard = false">取消</el-button>
                <el-button type="primary" @click="ConfirmCancel"
                    :disabled="cancelCardInfo.password.length === 0">确定</el-button>
            </span>
        </template>
        </el-dialog>

      <!--更新额度对话框-->
      <el-dialog v-model="UpdateLimit" title="更新额度" width="30%" align-center>
        <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
          输入密码：
          <el-input v-model="newUpdateLimit.password" style="width: 12.5vw;" clearable />
        </div>
        <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
          更新额度：
          <el-input v-model="newUpdateLimit.limit" style="width: 12.5vw;" clearable />
        </div>

        <template #footer>
                <span>
                    <el-button @click="this.UpdateLimit = false">取消</el-button>
                    <el-button type="primary" @click="ConfirmUpdateLimit"
                        :disabled="newUpdateLimit.account_id.length === 0 || newUpdateLimit.limit.length === 0">确定</el-button>
                </span>
            </template>
      </el-dialog>

      <!--更新密码对话框-->
      <el-dialog v-model="UpdatePassword" title="更新密码" width="30%" align-center>
        <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
          旧密码：
          <el-input v-model="newPassword.old_password" style="width: 12.5vw;" clearable />
        </div>
        <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
          新密码：
          <el-input v-model="newPassword.new_password" style="width: 12.5vw;" clearable />
        </div>

        <template #footer>
                <span>
                    <el-button @click="this.UpdatePassword=false">取消</el-button>
                    <el-button type="primary" @click="ConfirmUpdatePassword"
                        :disabled="newPassword.new_password.length === 0 || newPassword.old_password.length === 0">
                      确定</el-button>
                </span>
            </template>
      </el-dialog>

      <!--付款对话框-->
      <el-dialog v-model="PayBill" title="付款服务" width="30%" align-center>
            <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
                收款账号：
                <el-input v-model="newPayBill.PayTo_id" style="width: 12.5vw;" clearable />
            </div>
            <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
                支付金额：
                <el-input v-model="newPayBill.amount" style="width: 12.5vw;" clearable />
            </div>
            <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
                输入密码：
                <el-input v-model="newPayBill.password" style="width: 12.5vw;" clearable />
            </div>
            
            <template #footer>
                <span>
                    <el-button @click="this.PayBill = false">取消</el-button>
                    <el-button type="primary" @click="ConfirmPayBill"
                        :disabled="newPayBill.PayTo_id.length === 0
                        || newPayBill.amount.length === 0
                        || newPayBill.password.length === 0">确定</el-button>
                </span>
            </template>
        </el-dialog>

      <!--还款对话框-->
      <el-dialog v-model="RepayCredit" title="还款服务" width="30%" align-center>
          <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
              支付卡号：
              <el-input v-model="newRepayCredit.pay_account" style="width: 12.5vw;" clearable />
          </div>
          <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
              支付密码：
              <el-input v-model="newRepayCredit.pay_password" style="width: 12.5vw;" clearable />
          </div>
          <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
              还款金额：
              <el-input v-model="newRepayCredit.amount" style="width: 12.5vw;" clearable />
          </div>

          <template #footer>
              <span>
                  <el-button @click="this.RepayCredit = false">取消</el-button>
                  <el-button type="primary" @click="ConfirmRepayCredit"
                      :disabled="newRepayCredit.amount.length === 0 || newRepayCredit.pay_password.length === 0
                      || newRepayCredit.pay_account.length === 0">确定</el-button>
              </span>
          </template>
      </el-dialog>

      <!--查看月账单-->
      <el-dialog v-model="ViewBill" title="查看月账单" width="50%" align-center>
        <div style="display: flex;">
          <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px;">
            年份：
            <el-input v-model="billInfo.year" style="width: 8vw;" clearable />
          </div>
          <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px;">
            月份：
            <el-input v-model="billInfo.month" style="width: 6vw;" clearable />
          </div>
          <div style="margin-left: 2vw; margin-top: 20px; text-align: center;">
            <el-button type="primary" @click="ConfirmQueryBill">查询</el-button>
          </div>
          <div style="margin-left: 2vw; margin-top: 20px; text-align: center;">
          <el-button type="primary" @click="isShow=false,ViewBill=false">退出</el-button>
        </div>
        </div>

        <el-table v-if="isShow" :data="bills" :table-layout="'auto'"
          :default-sort="{ prop: 'date', order: 'ascending' }"
          style="width: 100%; margin-left: 10px; margin-top: 30px; margin-right: 50px; max-width: 80vw;">
          <el-table-column prop="bill_record_id" label="账单号" sortable />
          <el-table-column prop="account_in_id" label="付款账号" sortable />
          <el-table-column prop="account_out_id" label="收款账号" />
          <el-table-column prop="date" label="交易时间" />
          <el-table-column prop="amount" label="交易金额" />
        </el-table>
        <el-container v-if="isShow" style="margin-left: 1vw;font-weight: bold;">
          {{billInfo.year}} 年 {{billInfo.month}} 月 支出{{out_amount}}元，收入{{in_amount}}元，结余{{total_amount}}元
        </el-container>
      </el-dialog>

    </el-scrollbar>
  </template>

<script>
import axios from "axios";
import {ElMessage} from "element-plus";
import {
  Coin,
  CreditCard,
  DocumentDelete,
  ShoppingCart,
  List,
  Lock,
  Key,
  Close,
  Plus,
  View
} from "@element-plus/icons-vue";

export default{
  components: {View, Plus, Close, Key, CreditCard, List, Coin, ShoppingCart, DocumentDelete, Lock},
  data(){
    return{
      online_user_id: 1,
      creditcards: [
        {
          account_id: '',
          open_date: '',
          limit: 0.0,
          balance: 0.0,
          is_frozen: '',
          is_lost: '',
          card_type: '信用卡', // credit card
        },
      ],
      // apply new card
      newApplicationVisible: false,
      // see the apply list
      showApplyListVisible: false,
      showList: false,
      applyList: [
        {
          apply_id: '',
          apply_status: '',
          apply_result: '',
          apply_date: '',
          examiner_id: '',
          have_open: '',
        },
      ],
      // frozen
      freezeCreditVisible: false,
      newFreezeCredit: {
        account_id: '',
        password: '',
      },
      // report loss
      ReportLoss: false,
      newReportLoss: {
        account_id: '',
        password: '',
      },
      // cancel card
      CancelCard: false,
      cancelCardInfo: {
        account_id: '',
        password: ''
      },
      // update limits
      UpdateLimit: false,
      newUpdateLimit: {
        account_id: '',
        password: '',
        limit: 1500,
      },
      // update password
      UpdatePassword: false,
      newPassword: {
        account_id: 1,
        old_password: '',
        new_password: '',
      },
      // pay bill
      PayBill: false,
      newPayBill: {
        PayTo_id: '',
        account_id: '',
        amount: '',
        password: '',
      },
      // repay from other card
      RepayCredit: false,
      newRepayCredit: {
        account_id: '',
        pay_account:'' ,
        pay_password: '',
        amount: '',
      },
      // show month bill
      ViewBill: false,
      isShow: false, // 是否展示结果表格
      total_amount: 0,
      in_amount: 0,
      out_amount: 0,
      billInfo: {
        account_id: '',
        year: '',
        month: '',
      },
      bills: [
        {
          bill_record_id: '',
          account_in_id: '',
          account_out_id: '',
          amount: '',
          date: '',
        },
      ],
     newApplicationInfo:{
        annual_income:0.0,
        property_valuation:0.0,
        service_year:0,
      },
    }
  },
  methods: {
    QueryCards() {
      axios.get("/creditcard/get_cards", {
        params: {
          online_user_id: this.online_user_id
        }
      })
          .then(response => {
            this.creditcards = [];
            let tableData = response.data.list;
            tableData.forEach(item => {
              let card = {
                account_id: item.account_id,
                online_user_id: item.online_user_id,
                balance: item.balance,
                card_type: item.card_type,
                open_date: item.open_date,
                limit: item.credit_limit,
                is_frozen: item.is_frozen,
                is_lost: item.is_lost,
              };
              this.creditcards.push(card);
            });
          })
          .catch(error => {
                console.error('Error fetching examiners:', error);
                ElMessage.error("数据获取失败，请稍后重试！" + error);
          });
    },
    ConfirmFreezeCredit() {
      console.log("freeze:" + this.newFreezeCredit.account_id)
      axios.post("/creditcard/frozen_card",
      {
        account_id: this.newFreezeCredit.account_id,
        password: this.newFreezeCredit.password,
      })
          .then(response => {
            if (response.data.status === 'success') {
              ElMessage.success("冻结成功");
              this.freezeCreditVisible = false;
              this.QueryCards();
            } else {
              ElMessage.error("冻结失败: " + response.data.message);
            }
          })
          .catch(error => {
            console.error('Error ConfirmChangeState:', error);
            ElMessage.error("冻结失败：" + error);
          });
    },
    ConfirmReportLoss() {
      axios.post("/creditcard/lost_card",
      {
        account_id: this.newReportLoss.account_id,
        password: this.newReportLoss.password,
      })
          .then(response => {
            if (response.data.status === 'success') {
              ElMessage.success("挂失成功");
              this.ReportLoss = false;
              this.QueryCards();
            } else {
              ElMessage.error("挂失失败: " + response.data.message);
            }
          })
          .catch(error => {
            console.error('Error ConfirmChangeState:', error);
            ElMessage.error("挂失失败：" + error);
          });
    },
    ConfirmUpdateLimit() {
      // console.log("account_id:" + this.newUpdateLimit.account_id)
      axios.post("/creditcard/update_limit",
      {
        account_id: this.newUpdateLimit.account_id,
        password: this.newUpdateLimit.password,
        amount: this.newUpdateLimit.limit,
      })
          .then(response => {
            if (response.data.status === 'success') {
              ElMessage.success("更新成功");
              this.UpdateLimit = false;
              this.QueryCards();
            } else {
              ElMessage.error("更新失败: " + response.data.message);
            }
          })
          .catch(error => {
            console.error('Error ConfirmChangeState:', error);
            ElMessage.error("更新失败：" + error);
          });
    },
    ConfirmPayBill() {
      axios.post("/creditcard/pay_to",
      {
        account_out_id: this.newPayBill.account_id,
        account_in_id: this.newPayBill.PayTo_id,
        password: this.newPayBill.password,
        amount: this.newPayBill.amount,
      })
          .then(response => {
            if (response.data.status === 'success') {
              ElMessage.success("支付成功");
              this.PayBill = false;
              this.QueryCards();
            } else {
              ElMessage.error("支付失败: " + response.data.message);
            }
          })
          .catch(error => {
            console.error('Error ConfirmChangeState:', error);
            ElMessage.error("支付失败：" + error);
          });
    },
    ConfirmRepayCredit() {
      axios.post("/creditcard/repay",
      {
        account_id: this.newRepayCredit.account_id,
        pay_account: this.newRepayCredit.pay_account,
        pay_password: this.newRepayCredit.pay_password,
        amount: this.newRepayCredit.amount,
      })
          .then(response => {
            if (response.data.status === 'success') {
              ElMessage.success("还款成功");
              this.RepayCredit = false;
              this.QueryCards();
            } else {
              ElMessage.error("还款失败: " + response.data.message);
            }
          })
          .catch(error => {
            console.error('Error ConfirmChangeState:', error);
            ElMessage.error("还款失败：" + error);
          });
    },
    ConfirmQueryBill() {
      axios.get("/creditcard/show_month_bill", {
        params: {
          month: this.billInfo.month,
          year: this.billInfo.year,
          account_id: this.billInfo.account_id,
        }
      })
          .then(response => {
            this.bills = [];
            this.total_amount = response.data.total_amount;
            this.in_amount = response.data.in_amount;
            this.out_amount = response.data.out_amount;
            let tableData = response.data.list;
            tableData.forEach(item => {
              let bill = {
                bill_record_id: item.transfer_record_id,
                account_in_id: item.account_in_id,
                account_out_id: item.account_out_id,
                amount: item.transfer_amount,
                date: item.transfer_date,
              };
              this.bills.push(bill);
            });
            if (response.data.status === 'success') {
              ElMessage.success("查询成功");
              this.isShow = true;
              this.QueryCards();
            } else {
              ElMessage.error("查询失败: " + response.data.message);
            }
          })
          .catch(error => {
            ElMessage.error("查询失败：" + error);
          });
    },
    ConfirmApply() {
      axios.post("/creditcard/new_application", {
        online_user_id: this.online_user_id,
        annual_income: this.newApplicationInfo.annual_income,
        property_valuation: this.newApplicationInfo.property_valuation,
        service_year: this.newApplicationInfo.service_year,
      })
          .then(response => {
            if (response.data.status === 'success') {
              ElMessage.success("申请已提交");
              this.newApplicationVisible = false;
              this.QueryCards();
            } else {
              // console.log(this.online_user_id)
              ElMessage.error("申请提交失败: " + response.data.message);
            }
          })
          .catch(error => {
            // console.log(this.online_user_id)
            ElMessage.error("申请提交失败：" + error);
          });
    },
    ConfirmUpdatePassword() {
      axios.post("/creditcard/change_password", {
        account_id: this.newPassword.account_id,
        old_password: this.newPassword.old_password,
        new_password: this.newPassword.new_password
      })
          .then(response => {
            if (response.data.status === 'success') {
              ElMessage.success("修改成功");
              this.UpdatePassword = false;
              this.QueryCards();
            } else {
              ElMessage.error("修改失败: " + response.data.message);
            }
          })
          .catch(error => {
            ElMessage.error("修改失败：" + error);
          });
    },
    ConfirmCancel() {
      axios.post("/creditcard/cancel_card", {
        account_id: this.cancelCardInfo.account_id,
        password: this.cancelCardInfo.password
      })
          .then(response => {
            if (response.data.status === 'success') {
              ElMessage.success("取消成功");
              this.CancelCard = false;
              this.QueryCards();
            } else {
              ElMessage.error("取消失败: " + response.data.message);
            }
          })
          .catch(error => {
            ElMessage.error("取消失败：" + error);
          });
    },
    ConfirmShowApplyList() {
      console.log("show_list" + this.online_user_id)
      axios.get("/creditcard/get_application_at", {
        params: {
          online_user_id: this.online_user_id
        }
      })
          .then(response => {
            this.applyList = [];
            let tableData = response.data.list;
            tableData.forEach(item => {
              let apply = {
                apply_id: item.apply_id,
                apply_result: item.apply_result,
                apply_status: item.apply_status,
                apply_date: item.apply_date,
                examiner_id: item.examiner_id,
                have_open: item.have_open,
              };
              this.applyList.push(apply);
            })
            if (response.data.status === 'success') {
              ElMessage.success("查询成功");
              this.showList = true;
              this.QueryCards();
            } else {
              ElMessage.error("查询失败: " + response.data.message);
            }
          })
          .catch(error => {
            ElMessage.error("查询失败：" + error);
          });
    },
  },
  mounted() {
    this.QueryCards();
  }
}
</script>

<style scoped>
.creditcardBox {
  height:380px;
  width: 250px;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
  text-align: center;
  margin-top: 40px;
  margin-left: 28px;
  margin-right: 10px;
  padding: 15px 10px 8px 8px;
}
</style>