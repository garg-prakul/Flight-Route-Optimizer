from flight import Flight


class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        """Add an item to the end of the queue."""
        self.items.append(item)

    def dequeue(self):
        """Remove and return the item from the front of the queue."""
        if self.is_empty():
            raise IndexError("Dequeue from an empty queue")
        return self.items.pop(0)

    def is_empty(self):
        """Check if the queue is empty."""
        return len(self.items) == 0

    def peek(self):
        """Return the front item without removing it."""
        if self.is_empty():
            raise IndexError("Peek from an empty queue")
        return self.items[0]

    def size(self):
        """Return the number of items in the queue."""
        return len(self.items)


class Heap:
    
    
    def __init__(self, comparison_function, init_array):
        
        self.data= init_array
        self.comparator = comparison_function
        self.build_heap()
        
    def size(self):
        return len(self.data)   
       
    
    def insert(self, value):
       
        self.data.append(value)  
        i = self.size() - 1  
        while i > 0 and  self.comparator(self.data[i], self.data[self.parent(i)]):  
            self.data[i], self.data[self.parent(i)] = self.data[self.parent(i)], self.data[i]  
            i = self.parent(i) 

    def get_min(self):  
        if  self.size()> 0:  
            return self.data[0]  
        else:  
            return None  
        
        
     
    def extract(self):
       
        if self.size()==0:
            return None
        else:
            temp = self.data[0]
            self.data[0],self.data[len(self.data)-1] = self.data[len(self.data)-1],self.data[0]
            self.data.pop()
            self.heapify(0)
            return temp
        
        
        
    
    def top(self):
        
        if self.size() > 0:
            return self.data[0] 
        else:
            return None
       
    
   
    def parent(self, i):  
        return (i - 1) // 2  
    def left_child(self, i):  
        return 2 * i + 1  
    def right_child(self, i):  
        return 2 * i + 2  
    def build_heap(self):
        if(self.size()==0):
            return None
        else:
            for i in range(self.size() // 2 - 1, -1, -1): 
                self.heapify(i)

    def heapify(self, index):
        smallest = index
        left = 2 * index + 1
        right = 2 * index + 2

        if left < self.size() and self.comparator(self.data[left], self.data[smallest]):
            smallest = left

        if right < self.size() and self.comparator(self.data[right], self.data[smallest]):
            smallest = right

        if smallest != index:
            self.data[index], self.data[smallest] = self.data[smallest], self.data[index]
            self.heapify(smallest)
class Planner:
    def __init__(self, flights):
        """The Planner

        Args:
            flights (List[Flight]): A list of information of all the flights (objects of class Flight)
        """
        self.flight_list = flights
        self.m = len(flights)
        self.flight_adj_list = [[] for _ in range(self.m)]
        self.city_adj_list_out = [[] for _ in range(self.m)]
        self.city_adj_list_in = [[] for _ in range(self.m)]

        for flight in flights:
            self.city_adj_list_out[flight.start_city].append(flight)
            self.city_adj_list_in[flight.end_city].append(flight)

        for i, flight in enumerate(self.flight_list):
            for next_flight in self.city_adj_list_out[flight.end_city]:
                self.flight_adj_list[i].append(next_flight.flight_no)

    def least_flights_ealiest_route(self, start_city, end_city, t1, t2):
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying: 
        The route has the least number of flights, and within routes with same number of flights, 
        arrives the earliest
        """
        if start_city == end_city:
            return []

        start_flights = []
        results = []

        # Collect valid starting flights that depart after t1
        for flight in self.city_adj_list_out[start_city]:
            if flight.departure_time >= t1 and flight.arrival_time <= t2:
                start_flights.append(flight)

        if not start_flights:
            return []

        for starting_flight in start_flights:
            # Initialize predecessor and visited arrays
            predecessor = [-1] * self.m
            visited = [-1] * self.m

            visited[starting_flight.flight_no] = 0
            predecessor[starting_flight.flight_no] = -1

            # Use a deque for BFS to explore the flights
            main_queue = Queue()
            main_queue .enqueue((starting_flight.flight_no, starting_flight.arrival_time, 0))
            while not main_queue.is_empty():
                current_flight_no, current_time, num_flights = main_queue.dequeue()

                # Check if we reached the destination city
                if self.flight_list[current_flight_no].end_city == end_city:
                    path = []
                    time = self.flight_list[current_flight_no].arrival_time
                    a = current_flight_no
                    while a != -1:
                        
                        flight = self.flight_list[a]
                        path.append(flight)
                        a = predecessor[a]
                  
                    path.reverse()
                    results.append((path, len(path), time))
                    
                    

                # Explore all adjacent flights from the current flight's destination
                for next_flight_no in self.flight_adj_list[current_flight_no]:
                    next_flight = self.flight_list[next_flight_no]
                    dep_time = next_flight.departure_time

                    # Check if the next flight is valid based on the time window and buffer time
                    if dep_time >= current_time + 20 and dep_time >= t1 and next_flight.arrival_time <= t2 and visited[next_flight_no] != 0:
                        main_queue.enqueue((next_flight_no, next_flight.arrival_time, num_flights + 1))
                        visited[next_flight_no] = 0
                        predecessor[next_flight_no] = current_flight_no

      
        results.sort(key=lambda x: (x[1], x[2]))

       
        if results:
           
            return results[0][0]

        return []

    

   

    def cheapest_route(self, start_city, end_city, t1, t2):
       
        if start_city == end_city:
            return []
            
        possible_routes = []
        
        
        for starting_flight in self.city_adj_list_out[start_city]:
            
            if not (starting_flight.departure_time >= t1 and starting_flight.arrival_time <= t2):
                continue
                
           
            pq = []
            main_heap = Heap(lambda a,b:a[0] < b[0],pq)
            main_heap.insert((starting_flight.fare, starting_flight.flight_no, starting_flight.arrival_time))
            fare = [float('inf')] * self.m
            fare[starting_flight.flight_no] = starting_flight.fare
            predecessor = [-1] * self.m
            
            
            # Run Dijkstra's algorithm
            while main_heap.size()!=0:
               
                current_fare, current_flight, current_time = main_heap.extract()
                current_flight_obj = self.flight_list[current_flight]
                
               
                if current_flight_obj.end_city == end_city:
                    
                    path = []
                    current = predecessor[current_flight]
                    
                    path.append(self.flight_list[current_flight])
                    while current != -1:
                        path.append(self.flight_list[current])
                        current = predecessor[current]
                    possible_routes.append((fare[current_flight], path[::-1]))
                   
                    
               
                for next_flight_index in self.flight_adj_list[current_flight]:
                    next_flight = self.flight_list[next_flight_index]
                    if (next_flight.departure_time >= current_time + 20 and
                        next_flight.departure_time >= t1 and 
                        next_flight.arrival_time <= t2):
                        
                        new_fare = current_fare + next_flight.fare
                        if new_fare < fare[next_flight_index]:
                            fare[next_flight_index] = new_fare
                            predecessor[next_flight_index] = current_flight
                            main_heap.insert((new_fare, next_flight_index, next_flight.arrival_time))
        
      
        if possible_routes:
            return min(possible_routes, key=lambda x: x[0])[1]
        return []
                
    
    def least_flights_cheapest_route(self, start_city, end_city, t1, t2):
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying: 
        The route has the least number of flights, and within routes with same number of flights, 
        is the cheapest
        """
        if start_city == end_city:
            return []
            
        possible_routes = []
        
        
        for starting_flight in self.city_adj_list_out[start_city]:
            
            if not (starting_flight.departure_time >= t1 and starting_flight.arrival_time <= t2):
                continue
                
            pq = []
            main_heap = Heap(lambda a, b: (a[0], a[1]) < (b[0], b[1]), pq)

            main_heap.insert((0,starting_flight.fare, starting_flight.flight_no, starting_flight.arrival_time))
            
            fare = [float('inf')] * self.m
            num = [float('inf')] * self.m

            fare[starting_flight.flight_no] = starting_flight.fare
            num[starting_flight.flight_no] = 0
            predecessor = [-1] * self.m
            
            
            # Run Dijkstra's algorithm
            while pq:
               
                num_flights , current_fare, current_flight, current_time = main_heap.extract()
                current_flight_obj = self.flight_list[current_flight]
                
               
                if current_flight_obj.end_city == end_city:
                    
                    path = []
                    current = predecessor[current_flight]
                    
                    path.append(self.flight_list[current_flight])
                    while current != -1:
                        path.append(self.flight_list[current])
                        current = predecessor[current]
                    possible_routes.append((num_flights+1,fare[current_flight], path[::-1]))
                   
                    
               
                for next_flight_index in self.flight_adj_list[current_flight]:
                    next_flight = self.flight_list[next_flight_index]
                    if (next_flight.departure_time >= current_time + 20 and
                        next_flight.departure_time >= t1 and 
                        next_flight.arrival_time <= t2):

                        new_fare = current_fare + next_flight.fare
                        if num_flights +1 < num[next_flight_index]:
                            fare[next_flight_index] = new_fare
                            num[next_flight_index] = num_flights +1 
                            predecessor[next_flight_index] = current_flight
                            main_heap.insert((num[next_flight_index],new_fare, next_flight_index, next_flight.arrival_time))
        
      
        if possible_routes:
             possible_routes.sort(key=lambda x: (x[0], x[1]))
             return possible_routes[0][2]
        return []
                


        