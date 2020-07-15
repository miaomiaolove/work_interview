# -*- coding: utf-8 -*-
"""
解题思路：
    有五个结点（A - E）代表五个城市，城市直接可以连通。但是路线有方向。Graph: AB5, BC4, CD8, DC8, DE6, AD5, CE2, EB3, AE7
    AB5代表路线 A-B 路线长度==权重 5

    会有开始，结束的结点所有路线，但是需求满足：不能超过stops站的数量，距离也有限制不能超过最高权重。
    通过递归搜索，满足条件存放到列表中。

"""


# 单一路线
class SingleRoute(object):

    def __init__(self, fromStop, toStop, weight):
        self.fromStop = fromStop
        self.toStop = toStop
        self.weight = weight
        self.route = fromStop + toStop


# 单程路线的集合
class RouteSet(object):
    _routes = {}
    _exRouteIndex = {}

    #路线数据
    def __init__(self, routeData):
        self._routes = {}
        self._exRouteIndex = {}
        for route, weight in routeData.items():
            #检查格式
            if type(route) != str or len(route) != 2 or type(weight) != int:
                # 错误格式
                continue
            # 单一路线
            self._routes[route] = SingleRoute(route[0], route[1], weight)
        # 建立索引
        self._build_route_index()

    # 建立扩展路线的索引
    def _build_route_index(self):
        self.fromStops = {}
        toStops = []

        for sRoute in self._routes.values():
            if sRoute.fromStop not in self.fromStops:
                self.fromStops[sRoute.fromStop] = [sRoute]
            else:
                self.fromStops[sRoute.fromStop].append(sRoute)
            if sRoute.toStop not in toStops:
                toStops.append(sRoute.toStop)

        for fromStop, routeList in self.fromStops.items():
            for toStop in toStops:
                routeChain = self._extend_route(fromStop, toStop, [])
                if len(routeChain) > 0:
                    self._exRouteIndex[fromStop + toStop] = routeChain

    # 递归搜索
    def _extend_route(self, fromStop, toStop, chainRoute):
        result = []
        if fromStop not in self.fromStops:
            return result
        for elRoute in chainRoute:
            if fromStop == elRoute.fromStop:
                return result

        if fromStop + toStop in self._routes:
            option = chainRoute.copy()
            option.append(self._routes[fromStop + toStop])
            result.append(option)


        for childRoute in self.fromStops[fromStop]:
            option = chainRoute.copy()
            option.append(childRoute)
            nextStep = self._extend_route(childRoute.toStop, toStop, option)
            for aChain in nextStep:
                result.append(aChain)

        return result


    def exist(self, route):
        if route in self._routes:
            return True
        return False


    def get_weight(self, route):
        if self.exist(route):
            return self._routes[route].weight
        return 0

    def get_extend_routes(self, fromStop, toStop):
        if fromStop + toStop not in self._exRouteIndex:
            return []
        else:
            return self._exRouteIndex[fromStop + toStop]

# 搜索路线类
class SearchRoute(object):

    def __init__(self, rtData):
        if type(rtData) != dict:
           print( "param wrong type" )
        self.rtSet = RouteSet(rtData)

    #搜索权重
    def search_weight(self, stopList):
        weight = 0
        idx = 0
        while idx < len(stopList) - 1:
            route = stopList[idx] + stopList[idx + 1]
            if self.rtSet.exist(route):
                weight += self.rtSet.get_weight(route)
            else:
                return 'NO SUCH ROUTE'
            idx += 1

        return weight

    #搜索最小权重
    def search_shortest_weight(self, fromStop, toStop):
        shortestWeight = -1
        routeList = self.rtSet.get_extend_routes(fromStop, toStop)

        for route in routeList:
            weight = 0
            for nd in route:
                weight += nd.weight
            if shortestWeight < 0 or weight < shortestWeight:
                shortestWeight = weight

        return shortestWeight

    #搜索选项最大的权重
    def search_options_max_weight(self, fromStop, toStop, maxWeight):
        optionList = []
        routeList = self.rtSet.get_extend_routes(fromStop, toStop)

        for route in routeList:
            weight = 0
            for nd in route:
                weight += nd.weight
            if weight < maxWeight:
                optionList.append(route)
                childOptionList = self.search_options_max_weight(toStop, toStop, maxWeight - weight)
                for childRoute in childOptionList:
                    optionList.append(route + childRoute)

        return optionList

    #停止搜索选项
    def search_options_fix_stop(self, fromStop, toStop, fixStop):
        optionList = []
        routeList = self.rtSet.get_extend_routes(fromStop, toStop)

        for route in routeList:
            if len(route) > fixStop:
                continue
            elif len(route) == fixStop:
                if route in optionList:
                    continue
                optionList.append(route)
            else:

                childList = self.search_options_fix_stop(toStop, toStop, fixStop - len(route))
                for childRoute in childList:
                    if route + childRoute in optionList:
                        continue
                    optionList.append(route + childRoute)

        return optionList

    #停止搜索最大选项
    def search_options_max_stop(self, fromStop, toStop, maxStop):
        optionList = []
        routeList = self.rtSet.get_extend_routes(fromStop, toStop)
        for route in routeList:
            if len(route) > maxStop:
                continue
            optionList.append(route)

        return optionList


if __name__ == '__main__':
    """
    题目测试数据
    """
    data = {
        "AB": 5,
        "BC": 4,
        "CD": 8,
        "DC": 8,
        "DE": 6,
        "AD": 5,
        "CE": 2,
        "EB": 3,
        "AE": 7
    }
    sr = SearchRoute(data)
    # 1. A-B-C.
    print("Output #1: " + str(sr.search_weight(['A', 'B', 'C'])))

    # 2.  A-D.
    print("Output #2: " + str(sr.search_weight(['A', 'D'])))

    # 3.  A-D-C.
    print("Output #3: " + str(sr.search_weight(['A', 'D', 'C'])))

    # 4. A-E-B-C-D.
    print("Output #4: " + str(sr.search_weight(['A', 'E', 'B', 'C', 'D'])))

    # 5.  A-E-D.
    print("Output #5: " + str(sr.search_weight(['A', 'E', 'D'])))

    # 6. 从c 开始到c结束 有俩条行程 C-D-C   C-E-B-C
    options = sr.search_options_max_stop('C', 'C', 3)
    print("Output #6: " + str(len(options)))

    # 7. 从A 开始到C结束 A-C（经过B C D） A-C(经过D C D) A-C(D E B)
    options = sr.search_options_fix_stop('A', 'C', 4)
    print("Output #7: " + str(len(options)))

    # 8. A-C最短路线的长度
    print("Output #8: " + str(sr.search_shortest_weight('A', 'C')))

    # 9. B-B最短路线长度
    print("Output #9: " + str(sr.search_shortest_weight('B', 'B')))

    # 10.C-C距离小于30的不同路线 CDC、CEBC、CEBCDC、CDCEBC、CDEBC、CEBCEBC、CEBCEBC
    options = sr.search_options_max_weight('C', 'C', 30)
    print("Output #10: " + str(len(options)))