var token_key = 'uuid'
token = $.cookie(token_key)
if(token === undefined){
    if(!window.location.href.includes('/desktop/login')){
        alert('请登录')
        parent.window.location.href = '/desktop/login'
    }
}
if(!window.location.href.includes('/desktop/login')){
    $.ajaxSetup({
        beforeSend:function(xhr){
            xhr.setRequestHeader('Authorization', 'Token '+$.cookie(token_key))
        }
    })
}

function get_back(data){
  if('username' in data){
    return data['username']
  }else if('password' in data){
    return data['password']
  }else if('detail' in data){
    return data['detail']
  }else if('error' in data){
    return data['error']
  }
  else{
    return '未知错误'
  }
}

/**
 * linkmart 用户模块
 * 登录,注册,修改,列表
 */
function to_login(){
    submit_data = {}
    submit_data['username'] = $("input").eq(0).val()
    submit_data['password'] = $('input').eq(1).val()
    token = $.cookie('token')
    // if(typeof token === "undefined" || token === null){
    //   alert('请登录')
    // }
    // else{
    //   alert('已经登录')
    //   alert(token)
    // }
  $.ajax({
    url:'/userauth/login/',
    method:'POST',
    data:submit_data,
    async:true,
    success:function(data){
      alert('登录成功')
      if('access' in data){
        $.cookie('access', data['access'])
        $.cookie('refresh', data['refresh'])
        $.cookie('store_id', data['store_id'], {expires:7, path:'/'})
      }else if('uuid' in data){
        // expires 保留天数, path 路径
        $.cookie('uuid', data['uuid'], {expires:7, path:'/'})
        $.cookie('nid', data['nid'], {expires:7, path:'/'})
        $.cookie('store_id', data['store_id'], {expires:7, path:'/'})
      }
      window.location.href = '/'
    },
    error:function(err){
      data = err.responseJSON
      alert(get_back(data))
    }
  })
}
$('#to_login').click(function(){to_login()})

function to_register(){
  submit_data = {}
  input_label = $("form").eq(0).find("input")
  submit_data['username'] = input_label.eq(0).val()
  submit_data['email'] = input_label.eq(1).val()
  submit_data['password'] = input_label.eq(2).val()
  submit_data['password_again'] = input_label.eq(3).val()
  submit_data['store_id'] = $('form').eq(0).find('select').val()
  $.ajax({
    url:'/userauth/user/',
    method:'POST',
    data:submit_data,
    async:true,
    success:function(){
      alert('添加成功')
      now_page = 1
      get_users('list')
    },
    error:function(data){
      err = data.responseJSON
      alert(get_back(err))
    }
  })
}
$('#to_register').bind('click', to_register)

function get_users(action){
  /**
   * 获取用户信息
   * action:list/one 列表/个人
   */
  $("#user_list tbody").html('')
  $.ajax({
      url:(action == 'list') ? '/userauth/user/?ordering=-nid&page='+now_page : '/userauth/login/',
      method:'GET',
      async:true,
      success:function(data){
          if(action=='one'){
            each_data = [data]
          }else{
            each_data = data['results']
          }
          $.each(each_data, function(key, val){
            tr = $('<tr>')
            tr.append('<td>'+val['nid']+'</td>')
            tr.append('<td>'+val['username']+'</td>')
            tr.append('<td>'+'<span class="badge badge-success">'+val['store_name']['name']+'</span>'+'</td>')
            tr.append('<td>'+val['last_login']+'</td>')
            $("#user_list tbody").append(tr)
          })
      },
      error:function(data){
        err = data.responseJSON
        alert(err)
      }
    })
}

function update_password(){
  submit_data = {}
  input_label = $("form").eq(0).find("input")
  submit_data['password'] = input_label.eq(0).val()
  submit_data['new_password'] = input_label.eq(1).val()
  submit_data['confirm_password'] = input_label.eq(2).val()
  $.ajax({
    url:'/userauth/login/',
    method:'PUT',
    data:submit_data,
    async:true,
    success:function(){
      alert('修改成功')
    },
    error:function(data){
      err = data.responseJSON
      alert(get_back(err))
    }
  })
}
$('#update_password').bind('click', update_password)

/**
 * 
 * linkmart 门店模块
 * 列表,添加,修改
 */
function set_store_update(id){
  $.ajax({url:'/store/'+id,method:'GET',async:true,
    success:function(data){
      inputs = $('#put_lk_store').find('input')
      inputs.each(function(key, input){
        input.value = data[input.name]
      })
    },
    error:function(data){
      return get_back(data.responseJSON)
    }
  })
}
function get_store(action){
  /**
   * action: select, list   根据参数不同做不同的DOM操作
   */
  $.ajax({
    url:'/store/',
    method:'GET',
    async:true,
    success:function(data){
      if(action=='select'){
        selected = $('#register_store_id')
        $.each(data['results'], function(key, value){
            selected.append('<option value="'+value['id']+'">'+value['name']+'</option>')
        })
      }else if(action=='list'){
        tbody = $('#user_list tbody')
        tbody.html('')
        $.each(data['results'], function(key, val){
            h = $("<tr></tr>")
            h.append('<td>'+val['id']+'</td>')
            h.append('<td>'+val['name']+'</td>')
            h.append('<td><span class="badge badge-success">'+val['adds']+'</span></td>')
            h.append('<td><button class="btn btn-block btn-danger btn-xs" type="button" onclick="set_store_update('+val['id']+')">编辑</button></td>')
            tbody.append(h)
        })
      }
    },
    error:function(data){
      err = data.responseJSON
      alert(get_back(err))
    }
  })
}

function add_store(event){
  /**
   * 添加门店
   * event 获取不定参数
   */
  action = event.data.action
  if(action=='add'){
    form_number = 0
    method = 'POST'
    url = '/store/'
  }else{
    form_number = 1
    method = 'PUT'
    url = '/store/'+$('#display_id').val()
  }
    submit_data = {}
    input_label = $("form").eq(form_number).find("input")
    input_label.each(function(index, val){
      submit_data[val.name] = val.value
    })
  $.ajax({
    url:url,
    method:method,
    async:true,
    data:submit_data,
    success:function(data){
      alert('执行成功')
      get_store('list')
    },
    error:function(data){
      err = data.responseJSON
      alert(get_back(err))
    }
  })
}
// bind/on on是新版的bind 可以传参数
$('#to_add_store').on('click',{action:'add'}, add_store)
$("#to_up_store").on('click',{action:'put'}, add_store)


// 获取踩点数据
function get_area(){
  $.ajax({
    url:'/caidian/area/',
    method:'GET',
    async:false,
    success:function(data){
      map_data = data
      // area_list = data[1]
      // store_list = data[0]
    },
    error:function(data){
      err = data.ajaxSetup
      alert(get_back(err))
    }
  })
  return area_list
}
// 获取踩点门店标签
function get_label(){
  $.ajax({
    url:'/caidian/label/',
    method:'GET',
    async:false,
    success:function(data){
      //all_label 数据结构 [key:[name, score],...] 为地图使用
      //set_label(f_label) f_label 数据结构 [f_id:[label,label,..],...]
      f_label = []
      $.each(data, function(key, val){
        all_label[key+1] = [val.label_name, val.label_score]
        if(f_label[val.f_id] == undefined){
          f_label[val.f_id] = []
        }
        f_label[val.f_id].push(val)
      })
      set_label(f_label)
    },
    error:function(data){
      err = data.ajaxSetup
      alert(get_back(err))
    }
  })
  return all_label
}
// 添加踩点门店
function add_cd_store(){
  submit = {}
  input_list = $("#add_store").find('input')
  input_list.each(function(index, element){
      submit[element.name] = (element.value == '') ? 0 : element.value
  })
  select_list = $("#add_store").find('select')
  select_list.each(function(index, element){
    submit[element.name] = (element.value == '') ? 0 : element.value
  })
  $.ajax({
      url:'/caidian/store/',
      method:'POST',
      data:submit,
      async:true,
      success:function(){
          alert('添加成功')
      },
      error:function(data){
          err = data.responseJSON
          alert(get_back(err))
      }
  })
}
$('#add_cd_store').bind('click', add_cd_store)

// 获取标签选择情况
function get_label_checked(){
  checkboxs = $('#store_label').find('input')
  checked_list = []
  checkboxs.each(function(key, item){
    if(item.checked){
      checked_list.push(item.id)
    }
  })
  return checked_list.join(',')
}
// 修改踩点门店
function update_cd_store(){
  submit = {}
  input_list = $("#put_store").find('input')
  input_list.each(function(index, element){
      submit[element.name] = (element.value == '') ? 0 : element.value
  })
  select_list = $("#put_store").find('select')
  select_list.each(function(index, element){
    submit[element.name] = (element.value == '') ? 0 : element.value
  })
  submit['cd_label'] = get_label_checked()
  
  $.ajax({
      url:'/caidian/store/'+submit['store_id']+'/',
      method:'PUT',
      data:submit,
      async:true,
      success:function(){
          alert('修改成功')
      },
      error:function(data){
          err = data.responseJSON
          alert(get_back(err))
      }
  })
}
$("#update_cd_store").bind('click', update_cd_store)

// 保存踩点商圈
function save_cd_area(action){
  if(action=='add'){
    inputs = $('#add_cd_area').find('input')
  }else if(action=='put'){
    inputs = $('#put_cd_area').find('input')
  }
  submit_data = {}
  inputs.each(function(key, item){
    submit_data[item.name] = (item.value == '') ? 0 : item.value
  })
  alert(submit_data['id'])
  $.ajax({
    url:'/caidian/area/' + ((action == 'add') ? '':submit_data['id']+'/'),
    method:(action == 'add') ? 'POST':'PUT',
    data:submit_data,
    async:true,
    success:function(){
        alert('保存成功')
    },
    error:function(data){
        err = data.responseJSON
        alert(get_back(err))
    }
  })
}
$('#button_cd_area').bind('click', save_cd_area)

// 获取单个商圈数据 设置表单
function get_area_one(){
  $.ajax({
    url:'/caidian/area/'+this.value+'/',
    method:'GET',
    async:true,
    success:function(data){
      inputs = $('#put_cd_area').find('input')
      inputs.each(function(key, element){
        element.value = data[element.name]
      })
    },
    error:function(data){
        err = data.responseJSON
        alert(get_back(err))
    }
  })
}
$('#select_area').bind('change', get_area_one)

// 保存踩点数据
function save_cd_area(){
  inputs = $('#caidian_data').find('input')
  submit_data = {}
  inputs.each(function(key, item){
    if(item.name == 'cd_date'){
      the_value = item.value.split('/')
      submit_str = the_value[2] + '-' + the_value[0] +'-' + the_value[1]
    }else if (item.name == 'cd_stime'){
      time_str = item.value.split(' ')
      time_list = time_str[0].split(':')
      if(time_str[1] == 'PM'){
        time_list[0] = Number(time_list[0]) + 12
      }
      submit_str = time_list.join(':') + ':00'
    }
    else{
      submit_str = item.value
    }
    submit_data[item.name] = (submit_str == '') ? 0 : submit_str
  })
  $.ajax({
    url:'/caidian/data/',
    method:'POST',
    data:submit_data,
    async:true,
    success:function(){
        alert('保存成功')
    },
    error:function(data){
        err = data.responseJSON
        alert(get_back(err))
    }
  })
}
$("#add_cd_data").bind('click', save_cd_area)


/*
 * 爬虫模块
 */
var spider_id = ''
var ask_status = Object
// 启动爬虫
function run_spider(){
  $('#crawl').hide()
  $('#loading_img').show()
  categoryId = $('#children_classify').val()
  $.ajax({
    url:'/runspider/orderform/',
    method:'GET',
    data:{'spider_name':'goods', 'last_goods':0, 'categoryId':categoryId},
    async:true,
    success:function(data){
        alert('发出启动信号...')
        spider_id = data['id']
    },
    error:function(data){
        err = data.responseJSON
        alert(get_back(err))
    }
  })
  ask_status = setInterval(function(){
    ask_spider_status(spider_id)
  }, 3000)
}
spider_status = ''
//获取爬虫状态
function ask_spider_status(spider_id){
  $.ajax({
    url:'/runspider/orderform/',
    method:'POST',
    data:{'id':spider_id},
    async:true,
    success:function(data){
        spider_status = data['status']
        if(data['status'] == 'SUCCESS'){
          $('#crawl').show()
          $('#loading_img').hide()
          alert('爬取成功')
          get_goods()
          clearInterval(ask_status)
        }
    },
    error:function(data){
        err = data.responseJSON
        alert(get_back(err))
        clearInterval(ask_status)
    }
  })
}

function get_data(url, data, call_back=null){
  var result_data = {}
  $.ajax({
    url:url,
    method:'GET',
    data:data,
    async:true,
    success:function(data){
      result_data = data
      if(call_back!=null){
        call_back(data)
      }
    },
    error:function(data){
        err = data.responseJSON
        alert(get_back(err))
    }
  })
  return result_data
}

function post_data(url, data, call_back=null){
  var result_data = {}
  $.ajax({
    url:url,
    method:'POST',
    data:data,
    async:true,
    success:function(data){
      result_data = data
      if(call_back!=null){
        call_back(data)
      }
    },
    error:function(data){
        err = data.responseJSON
        alert(get_back(err))
    }
  })
  return result_data
}

function put_data(url, data, call_back=null){
  var result_data = {}
  $.ajax({
    url:url,
    method:'PUT',
    data:data,
    async:true,
    success:function(data){
      result_data = data
      if(call_back!=null){
        call_back(data)
      }
    },
    error:function(data){
        err = data.responseJSON
        alert(get_back(err))
    }
  })
  return result_data
}


//热力图标
function hotmap(chart_doc, all_data, chart_name){
  const hours = []
  for(i=0;i<24;i++){
      hours.push(i)
  }
  // prettier-ignore
  const days = [
      '星期一', '星期二', '星期三',
      '星期四', '星期五', '星期六', '星期天'
  ];
  // prettier-ignore
  const data = all_data.map(function (item) {
      return [item[1], item[0], parseInt(item[2]) || '-'];
  });
//    for(key in data){
//        document.write(data[key]+"<br />")
//    }
  option = {
    tooltip: {
      position: 'top'
    },
    grid: {
      height: '65%',
      top: '5%',
      bottom: '5%',
      width: '90%',
      left:'center',
    },
    xAxis: {
      type: 'category',
      data: hours,
      splitArea: {
        show: true
      }
    },
    yAxis: {
      type: 'category',
      data: days,
      splitArea: {
        show: true
      }
    },
    visualMap: {
      min: 0,
      max: 60,
      calculable: true,
      orient: 'horizontal',
      left: 'center',
      bottom: '5%'
    },
    series: [
      {
        name: '商品数',
        type: 'heatmap',
        data: data,
        label: {
          show: true
        },
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  };
  chart_doc.setOption(option)
}

// 普通图表
function set_charts(chart_doc, all_data, x_list, chart_name, legend_list){
  /*
      all_data Y轴数据[{name:X,type:line/bar,data:[x,..]},{}]
  */
  var option = {
      title: {
          text: chart_name        //图表标题
      },
      // tooltip: {
      //     trigger: 'axis',
      //     axisPointer: {
      //       type: 'shadow',
      //       label: {
      //         show: true
      //       }
      //     }},
      tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'cross',
            label: {
                backgroundColor: '#6a7985'
            }
        }
      },
      legend: {
          data:legend_list,       //头部导航[名称，..]
          right:0,
      },
      toolbox: {
        feature: {
            saveAsImage: {show:false}
        }
      },    
      grid: {                     // 图表属性
        top: '8%',
        bottom: '5%',
        width: '95%',
        left:'center',
      },
      xAxis: {
          type:'category',
          data: x_list            // X坐标数据
      },
      yAxis: {},
      series: all_data            // Y轴数据[{name:X,type:line/bar,data:[x,..]},{}]
  };
  chart_doc.setOption(option)
}

// 普通竖图表
function set_charts_stand(chart_doc, all_data, x_list, chart_name, legend_list){
  /*
      all_data Y轴数据[{name:X,type:line/bar,data:[x,..]},{}]
  */
  var option = {
      title: {
          text: chart_name        //图表标题
      },
      // tooltip: {
      //     trigger: 'axis',
      //     axisPointer: {
      //       type: 'shadow',
      //       label: {
      //         show: true
      //       }
      //     }},
      tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'cross',
            label: {
                backgroundColor: '#6a7985'
            }
        }
      },
      legend: {
          data:legend_list,       //头部导航[名称，..]
          right:0,
      },
      toolbox: {
        feature: {
            saveAsImage: {show:false}
        }
      },    
      grid: {                     // 图表属性
        top: '5%',
        bottom: '5%',
        width: '80%',
        left:'center',
      },
      yAxis: {
          type:'category',
          data: x_list            // X坐标数据
      },
      xAxis: {},
      series: all_data            // Y轴数据[{name:X,type:line/bar,data:[x,..]},{}]
  };
  chart_doc.setOption(option)
}