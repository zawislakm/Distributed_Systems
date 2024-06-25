import sys
from concurrent.futures import ThreadPoolExecutor

from grpc_reflection.v1alpha import reflection

sys.path.append("gen")

from gen.store_pb2 import *
from gen.store_pb2_grpc import *


# https://github.com/grpc/grpc/blob/master/examples/python/helloworld/greeter_server_with_reflection.py

def merge_baskets(new_basket: Basket, old_basket: Basket) -> Basket:
    for item in new_basket.items:
        if item in old_basket.items:
            old_basket.amounts[item] += new_basket.amounts[item]
        else:
            old_basket.items.append(item)
            old_basket.amounts[item] = new_basket.amounts[item]

    return old_basket


class StoreService(StoreServiceServicer):
    orders_count = 1
    orders = {}

    def GetOrder(self, get_order_request: GetOrderRequest, context) -> Order:
        print("Server received request: GET ORDER")
        print(f"Request: {get_order_request}")
        print()

        if get_order_request.id < 1:
            context.set_details(f"Order id: {get_order_request.id} is invalid value")
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return Order()
        elif get_order_request.id not in self.orders.keys():
            context.set_details(f"Order id: {get_order_request.id} no order with this id")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return Order()
        else:
            return self.orders.get(get_order_request.id)

    def CreateOrder(self, new_order_request: Order, context) -> Order:
        print("Server received request: CREATE ORDER")
        print(f"Request: {new_order_request}")
        print()

        if new_order_request.id in self.orders.keys():
            context.set_details(f"Order id: {new_order_request.id} is already used")
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            return Order()
        elif new_order_request.id < 0:
            context.set_details(f"Order id: {new_order_request.id} must be 1 or higher")
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return Order()

        elif new_order_request.id == 0:
            new_order_request.id = self.orders_count
            self.orders[self.orders_count] = new_order_request
            self.orders_count += 1
            return new_order_request

    def AddItemsToOrder(self, update_order_request: UpdateOrderRequest, context) -> Order:
        print("Server received request: ADD ITEMS TO ORDER")
        print(f"Request: {update_order_request}")
        print()

        if update_order_request.id in self.orders.keys():

            order = self.orders.get(update_order_request.id)
            old_basket = order.basket
            new_basket = update_order_request.basket

            new_order = Order(id=order.id, basket=merge_baskets(old_basket, new_basket), address=order.address,
                              client=order.client)

            self.orders[order.id] = new_order
            return new_order

        else:
            context.set_details(f"Order id: {update_order_request.id} no order with this id")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return Order()


def serve():
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    add_StoreServiceServicer_to_server(StoreService(), server)

    SERVICE_NAMES = (
        DESCRIPTOR.services_by_name['StoreService'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    server.add_insecure_port('[::]:50051')
    print("Server Started")
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
