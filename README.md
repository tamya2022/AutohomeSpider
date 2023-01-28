<h3 align="center">selenium学习案例</h3>

## cookie
1. 获取所有cookie
    driver.get.cookies（）
    返同列表格式字典类型 [{},{},{}]
    
2. 添加cookie(需要逐条添加)
    driver.add_cookie（参数）
    参数：字典格式{"name":"name值","value":"value值"}

3. 启动含缓存的chrome浏览器
这种方式启动浏览器需要注意，运行代码前需要关闭所有的正在运行 chrome 程序，不然会报错。     
启动后会发现之前保存的书签、收藏夹。
```
profile_directory = r'--user-data-dir={}\AppData\Local\Google\Chrome\User Data'.format(my_dir)
option.add_argument(profile_directory)
```

## 获取元素信息
```
# 获取文本
element.text
# 其他属性
element.get_attribute("class")
# 输入的内容
element.get_attribute("value")
```

## 选项卡管理
```
browser.switch_to.frame("iframe的id")
# 切换到父frame
browser.switch_to.parent_frame()
# 增加新标签页
browser.execute_script('window.open()')
# 输出标签页信息
browser.window_hanlers
# 切换到标签页1
browser.switch_to.window(browser.window_handles[1])
# 切换到当前最新打开的窗口
driver.switch_to.window(windows[-1])
# 关闭当前标签页
browser.close()
# 退出浏览器
browser.quit()
```

