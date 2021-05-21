#include "hwlib.hpp"
#include "main.hpp"

extern "C" void print_asciz( const char *s[] ){
   hwlib::cout << s << hwlib::endl;
}

extern "C" void uart_print_int( uint32_t num ){
   hwlib::cout << num << hwlib::endl;
}

extern "C" uint32_t uart_get_int(void){
   uint32_t num = 5;
   // hwlib::cin >> num;
   return num;
}

int main( void ){

   namespace target = hwlib::target;

      // wait for the PC console to start
   hwlib::wait_ms( 2000 );
   hwlib::cout << "Starting..." << hwlib::endl;

   application();
   hwlib::cout << "Exiting..." << hwlib::endl;
}
