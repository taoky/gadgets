离散事件设计（对战类游戏）

每名玩家包含一个「冷却时间」（`freezeTime`）属性，只有在冷却时间结束后，才能释放下一个技能（用户输入事件），释放技能的顺序由 `eventSeq` 决定；若在相同的时间片内有不同的事件，则顺序决定于玩家的 `priority`（事件发生顺序可能会对结果带来较大的影响）。若该玩家 HP 已经 <= 0，那么不执行对应的事件。总计包含 4 类事件：

1. `attack`: 某名玩家以某种规则攻击另一名玩家。
   1. 攻击方式
      1. `physical`: 物理攻击，对应被攻击者的物理防御。
      2. `magical`: 魔法攻击，对应被攻击者的魔法防御。
   2. 攻击策略
      1. `leastHp`: 攻击 HP 最小的玩家。
      2. `leastPd`: 攻击物理防御最小的玩家。
      3. `leastMp`: 攻击 MP 最小的玩家。
      4. `leastMd`: 攻击模仿防御最小的玩家。
   3. 最小攻击值、最大攻击值：实际攻击值在两值内随机产生。
   4. 概率
   5. 附录
      1. 攻击计算方法：`max{攻击值 - 0.1 * 对方对应防御值, 1}`
2. `heal`: 某名玩家以一定的代价恢复自己的 HP 或 MP。
   1. 恢复内容
      1. `hp`: 以 MP 换 HP（MP 可以为 0）
      2. `mp`: 以 HP 换 MP（HP 可以为 0）
   2. 增加值
   3. 代价
   4. 概率
3. `magic`: 某名玩家以一定的 MP 在指定时间内临时增加自己的攻击或防御。
   1. 增加属性
      1. `pa`: 物理攻击偏移
      2. `pd`: 物理防御偏移
      3. `ma`: 魔法攻击偏移
      4. `md`: 魔法防御偏移
   2. 需要的 MP
   3. 得到的属性偏移
   4. 持续时间片
   5. 概率
4. `return`: 由 `magic` 生成的事件，不由用户输入，恢复玩家属性到正常。
   1. 恢复的属性：与 `magic` 增加属性相同。置 0。