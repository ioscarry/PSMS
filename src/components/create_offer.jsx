import React from "react";
import {AjaxSelect} from "./select";
import {DateSingle,Daterange} from "./daterange";
require("../lib/price-calendar");

var CreateOffer = React.createClass({
    componentDidMount(){
        $("#price-calendar").priceCalendar();
        $(".calendar_img").click(function () {
            $(".price-calendar").show();
        });
        $(".cal-save").on("click",function () {
            $(".price-calendar").hide();
        })
        $(".cal-cancel").on("click",function () {
            $(".price-calendar").hide();
        })
    },
    render:function () {
        return (
            <div id="create_offer" className="row">
                <div className="col-sm-10">
                    <div className="col-sm-3 text-right">
                        客户名称
                    </div>
                    <div className="col-sm-3">
                        <select className="form-control">
                            <option>aaa</option>
                            <option>aaa</option>
                        </select>
                    </div>
                    <div className="col-sm-3 text-right">
                        Status
                    </div>
                    <div className="col-sm-3">
                        <select className="form-control">
                            <option>Inactive</option>
                            <option>Active</option>
                        </select>
                    </div>
                </div>
                <div className="col-sm-10">
                    <div className="col-sm-3 text-right">
                        合作方式
                    </div>
                    <div className="col-sm-3">
                        <select className="form-control">
                            <option>服务费</option>
                            <option>aaa</option>
                        </select>
                    </div>
                    <div className="col-sm-3 text-right">
                        比例
                    </div>
                    <div className="col-sm-3">
                        <input type="text" className="form-control"/>
                    </div>
                </div>
                <div className="col-sm-10">
                    <div className="col-sm-3 text-right">
                        合同编号
                    </div>
                    <div className="col-sm-3">
                        <input type="text" className="form-control"/>
                    </div>
                    <div className="col-sm-3 text-right">
                        销售
                    </div>
                    <div className="col-sm-3">
                        <input type="text" className="form-control"/>
                    </div>
                </div>
                <div className="col-sm-12">
                    <hr/>
                </div>
                <div className="col-sm-10">
                    <div className="col-sm-3 text-right">
                        操作系统
                    </div>
                    <div className="col-sm-3">
                        <select className="form-control">
                            <option>IOS</option>
                            <option>Android</option>
                        </select>
                    </div>
                    <div className="col-sm-3 text-right">
                        包名
                    </div>
                    <div className="col-sm-3">
                        <input type="text" className="form-control"/>
                    </div>
                </div>
                <div className="col-sm-10">
                    <div className="col-sm-3 text-right">
                        APP 名称
                    </div>
                    <div className="col-sm-9">
                        <input type="text" className="form-control"/>
                    </div>
                </div>
                <div className="col-sm-10">
                    <div className="col-sm-3 text-right">
                        APP 类型
                    </div>
                    <div className="col-sm-9">
                        <input type="text" className="form-control"/>
                    </div>
                </div>
                <div className="col-sm-10">
                    <div className="col-sm-3 text-right">
                        Preview Link
                    </div>
                    <div className="col-sm-9">
                        <input type="text" className="form-control"/>
                    </div>
                </div>
                <div className="col-sm-10">
                    <div className="col-sm-3 text-right">
                        Tracking Link
                    </div>
                    <div className="col-sm-9">
                        <input type="text" className="form-control"/>
                    </div>
                </div>
                <div className="col-sm-12">
                    <hr/>
                </div>
                <div className="col-sm-10">
                    <div className="col-sm-3 text-right">
                        制作素材
                    </div>
                    <div className="col-sm-3">
                       <select　className="form-control">
                           <option>Yes</option>
                           <option>No</option>
                       </select>
                    </div>
                </div>
                <div className="col-sm-10">
                    <div className="col-sm-3 text-right">
                        投放起始
                    </div>
                    <div className="col-sm-3">
                        <DateSingle id="start_date" keyword="start_date"/>
                    </div>
                    <div className="col-sm-3 text-right">
                        投放截止
                    </div>
                    <div className="col-sm-3">
                        <DateSingle id="end_date" keyword="end_date"/>
                    </div>
                </div>
                <div className="col-sm-10">
                    <div className="col-sm-3 text-right">
                        投放平台
                    </div>
                    <div className="col-sm-9">
                        <AjaxSelect className="tfpt" placeholder="投放平台"　multiple="true" url="https://api.github.com/search/repositories" />
                    </div>
                </div>
                <div className="col-sm-10">
                    <div className="col-sm-3 text-right">
                        投放地区
                    </div>
                    <div className="col-sm-9">
                        <AjaxSelect className="tfdq" placeholder="投放地区．．．"　multiple="true" url="https://api.github.com/search/repositories" />
                    </div>
                </div>
                <div className="col-sm-10">
                    <div className="col-sm-3 text-right">
                        投放单价
                    </div>
                    <div className="col-sm-9">
                        <button　className="btn btn-primary">Import</button>
                    </div>
                </div>
                <div className="col-sm-10">
                    <div className="col-sm-3"> </div>
                    <div className="col-sm-9 table-responsive">
                        <table className="table table-bordered text-center">
                            <tbody>
                                <tr>
                                    <td>US</td>
                                    <td><input type="number" className="form-control" /></td>
                                    <td><img className="calendar_img" style={{cursor:"pointer"}} src="./src/img/calender.jpg"/></td>
                                </tr>
                                <tr>
                                    <td>US</td>
                                    <td><input type="number" className="form-control" /></td>
                                    <td><img className="calendar_img" style={{cursor:"pointer"}} src="./src/img/calender.jpg"/></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
                <div className="col-sm-10">
                    <div className="col-sm-3 text-right">
                        最高日预算
                    </div>
                    <div className="col-sm-3">
                        <select className="form-control">
                            <option>Install</option>
                            <option>Cost</option>
                        </select>
                    </div>
                    <div className="col-sm-3">
                        <input type="text" className="form-control"/>
                    </div>
                </div>
                <div className="col-sm-10">
                    <div className="col-sm-3 text-right">
                        最高总预算
                    </div>
                    <div className="col-sm-3">
                        <select className="form-control">
                            <option>Install</option>
                            <option>Cost</option>
                        </select>
                    </div>
                    <div className="col-sm-3">
                        <input type="text" className="form-control"/>
                    </div>
                </div>
                <div className="col-sm-10">
                    <div className="col-sm-3 text-right">
                        预算分配
                    </div>
                    <div className="col-sm-9">
                        <input type="text" className="form-control"/>
                    </div>
                </div>
                <div className="col-sm-10">
                    <div className="col-sm-3 text-right">
                        授权账户
                    </div>
                    <div className="col-sm-9">
                        <input type="text" className="form-control"/>
                    </div>
                </div>
                <div className="col-sm-10">
                    <div className="col-sm-3 text-right">
                        命名规则
                    </div>
                    <div className="col-sm-9">
                        <input type="text" className="form-control"/>
                    </div>
                </div>
                <div className="col-sm-12">
                    <hr/>
                </div>
                <div className="col-sm-10">
                    <div className="col-sm-3 text-right">
                        KPI　要求
                    </div>
                    <div className="col-sm-9">
                        <input type="text" className="form-control"/>
                    </div>
                </div>
                <div className="col-sm-10">
                    <div className="col-sm-3 text-right">
                        结算标准
                    </div>
                    <div className="col-sm-9">
                        <input type="text" className="form-control"/>
                    </div>
                </div>
                <div className="col-sm-10">
                    <div className="col-sm-3 text-right">
                        账期
                    </div>
                    <div className="col-sm-9">
                        <input type="text" className="form-control"/>
                    </div>
                </div>
                <div className="col-sm-12">
                    <hr/>
                </div>
                <div className="col-sm-10">
                    <div className="col-sm-3 text-right">
                        备注
                    </div>
                    <div className="col-sm-9">
                        <textarea className="form-control">

                        </textarea>
                    </div>
                </div>
                <div className="col-sm-12">
                    <hr/>
                </div>
                <div className="col-sm-10">
                    <div className="col-sm-3 text-right">
                        邮件报告
                    </div>
                    <div className="col-sm-9">
                        <select className="form-control">
                            <option>15:30</option>
                        </select>
                    </div>
                </div>
                <div className="col-sm-10">
                    <div className="col-sm-3 text-right">

                    </div>
                    <div className="col-sm-9">
                        <input type="text" className="form-control" placeholder="xx@xx.com,xx@xx.com"/>
                    </div>
                </div>
                <div className="col-sm-10">
                    <div className="col-sm-3 text-right">
                        报告模板
                    </div>
                    <div className="col-sm-9">
                        <select className="form-control">
                            <option>最全数据模板</option>
                        </select>
                    </div>
                </div>
                <div className="col-sm-10">
                    <div className="col-sm-3 text-right">

                    </div>
                    <div className="col-sm-9">
                        <button className="btn btn-primary">Create/Update</button>
                        <button className="btn btn-warning" style={{marginLeft:"20px"}}>Cancel</button>
                    </div>
                </div>
                <div className="mask price-calendar">
                    <div className="mask_mask box-center">
                        <div id="price-calendar"></div>
                    </div>
                </div>
            </div>
        )
    }
});
export default  CreateOffer;