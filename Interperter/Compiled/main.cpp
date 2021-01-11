#include "hwlib.hpp"
#include "main.hpp"

extern "C" void uart_print_string( *char[] str ){
   hwlib::cout << str << std::endl;
}

extern "C" void uart_print_int( uint32_t num ){
   hwlib::cout << num << std::endl;
}

extern "C" uint32_t uart_get_int(void){
   uint32_t num;
   hwlib::cin >> num;
   return num
}

int main( void ){

   namespace target = hwlib::target;

      // wait for the PC console to start
   hwlib::wait_ms( 2000 );
   hwlib::cout << "Starting..." << std::endl;

   application();
   hwlib::cout << "Exiting..." << std::endl;
}
