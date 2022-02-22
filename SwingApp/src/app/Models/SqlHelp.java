package app.Models;

import java.io.*;
import java.util.*;

    public class SqlHelp {
        private final LinkedHashMap<String, HashMap<String, HashMap<String,String>>> coreMap = new LinkedHashMap<String, HashMap<String, HashMap<String,String>>>();
        private String ptrSection = null;
        private String filePath;
        private boolean isChange = false;


        /**
         * 读取
         */
        public SqlHelp(){
            this("src/app/Models/data.ini");
        }

        /***
         * 读取
         * 
         * @param path
         * @throws IOException
         */
        public SqlHelp(String path) {
            filePath = path;
            try {
                init();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }

        // #region 构建链表

        /**
         * 初始化链表
         * 
         * @throws IOException
         */
        private void init() throws IOException {
            coreMap.clear();
            var reader = new BufferedReader(new InputStreamReader(new FileInputStream(filePath), "UTF-8"));
            String line = null;
            while ((line = reader.readLine()) != null) {
                parseLine(line);
            }
            reader.close();
        }

        /**
         * 转换
         * 
         * @param line
         */
        private void parseLine(String line) {
            line = line.trim();
            // 注释
            // if (line.matches("^\\#.*$")) {
            //     return;
            // } else 
            if (line.matches("^\\[\\S+\\]$")) {
                // section
                String section = line.replaceFirst("^\\[(\\S+)\\]$", "$1");
                addSection(section);
            } else if (line.matches("^\\S+=.*$")) {
                // key ,value
                int i = line.indexOf("=");
                String key = line.substring(0, i).trim();
                String kvalue = line.substring(i + 1).trim();
                addKeyValue(ptrSection, key, kvalue);
            }
        }

        /**
         * 增加新的Key和Value
         * 
         * @param currentSection
         * @param key
         * @param value
         */
        private void addKeyValue(String ptrSection, String key, String value) {
            if (!coreMap.containsKey(ptrSection)) {
                return;
            }
            HashMap<String,String> temp=new HashMap<>();
            for (String kv : value.split("_")) {
                temp.put(kv.split(":")[0], kv.split(":")[1]);
            }
            Map<String, HashMap<String, String>> childMap = coreMap.get(ptrSection);
            childMap.put(key, temp);
        }

        /**
         * 添加Section
         * 
         * @param section
         */
        private void addSection(String section) {
            if (!coreMap.containsKey(section)) {
                ptrSection = section;
                LinkedHashMap<String, HashMap<String, String>> childMap = new LinkedHashMap<String, HashMap<String, String>>();
                coreMap.put(section, childMap);
            }
        }

        // #endregion

        // #region 增
        /**
         * 添加键值对到指定的section
         * 
         * @param ptrSection
         * @param key
         * @param value
         */
        public void insert(String section, String key, String value) {
            addKeyValue(section, key, value);
            isChange = true;
        }

        public void insert(String section, String num, String key,String value) {
            select(section, num).put(key, value);
            isChange = true;
        }
        // #endregion

        // #region 删
        /**
         * 删除指定section下的指定键值对
         *
         * @param ptrSection
         * @param key
         */
        public void del(String section, String key) {
            if (coreMap.containsKey(section)) {
                coreMap.get(section).remove(key);
            }
            isChange = true;
        }

        public void del(String section, String key,String item) {
            if (coreMap.containsKey(section)) {
                coreMap.get(section).get(key).remove(item);
            }
            isChange = true;
        }


        // #endregion

        // #region 改
        /**
         * 修改指定section下的指定key的值为newValue
         * 
         * @param ptrSection
         * @param key
         * @param newValue
         */
        public void updata(String section, String key,String item ,String newValue) {
            coreMap.get(section).get(key).put(item, newValue);
            isChange = true;
        }
        // #endregion

        // #region 查

        /**
         * 查询指定section下指定key的item
         * 
         * @param section
         * @param key
         * @param item
         * @return
         */
        public String select(String section, String key,String item) {
            return select(section, key)==null?null:select(section, key).containsKey(item)?select(section, key).get(item):null;
        }

        /**
         * 获取配置文件指定Section和指定子键的值
         * 
         * @param section
         * @param key
         * @return
         */
        public Map<String,String> select(String section, String key) {
            return select(section)==null?null:select(section).containsKey(key)?select(section).get(key):null;
        }

        /**
         * 获取配置文件指定Section的子键和值
         * 
         * @param section
         * @return
         */
        public Map<String, HashMap<String, String>> select(String section) {
            return coreMap.containsKey(section) ? coreMap.get(section) : null;
        }

        /**
         * 获取这个配置文件的节点和值
         * 
         * @return
         */
        public LinkedHashMap<String, HashMap<String, HashMap<String, String>>> select() {
            return coreMap;
        }

        // #endregion

        // #region 存储
        private void save() {
            try {
                BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(filePath), "UTF-8"));
                for (var kv : coreMap.entrySet()) {
                    writer.write("[" + kv.getKey() + "]\r\n");
                    for (var childMap : kv.getValue().entrySet()) {
                        String temp="";
                        for (var item : childMap.getValue().entrySet()) {
                            temp+=item.getKey()+":"+item.getValue()+"_";
                        }
                        writer.write(childMap.getKey() + "=" + temp + "\r\n");
                    }
                }
                writer.flush();
                writer.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }

        /**
         * 关闭
         */
        public void close() {
            if (isChange) {
                save();
            }
        }

        // #endregion

        /**
         * 测试部分功能
         * 
         * @param args
         */
        public static void main(String[] args) {
            SqlHelp sqlHelp = new SqlHelp("src/app/Models/data.ini");
            System.out.println(sqlHelp.select("teacher", "79920420","密码"));
            //sqlHelp.del("teacher", "79920420","密码");
            //sqlHelp.updata("teacher", "79920420", "密码","12356");
            sqlHelp.close();
        }

    }