uint16_t phi;     
uint16_t theta;     
uint16_t psi;       
uint16_t gamma;     

void init();
void contract();

void move();
void back();
void sweep();
void stabilise();
void pickup();

/*  
    servos      angles  CLCx    PORTC
    base:       phi     CLC1    PC0
    shoulder:   theta   CLC2    PC1
    elbow:      psi     CLC3    PC2
    tweezers:   gamma   CLC4    PC3
*/

void CLCxOnly(int x);

void main() {

    while (1)
    {
        sweep();
        stabilise();

        if (getch() == 'j') {
            pickup();
        }

        if (getch() == 't') {
            contract();
            intial();
        }
    }

}

void init() {

    /* to fill in */
    int phi_init = ;
    int theta_init = ;
    int psi_init = ;
    int gamma_init = ;

    int initValues[] = {phi_init, theta_init, psi_init, gamma_init}

    for(int i=0; i<4; i++) {
        CLCxOnly(i+1);
        TMR6_Period8BitSet(initValues[i]);
    }

    __delay_ms(1500);
}

void contract() {

    /* to fill in */
    int phi_cont = ;
    int theta_cont = ;
    int psi_cont = ;
    int gamma_cont = ;

    int contValues[] = {phi_cont, theta_cont, psi_cont, gamma_cont}
    
    for(int i=0; i<4; i++) {
        CLCxOnly(i+1);
        TMR6_Period8BitSet(contValues[i]);
    }

    __delay_ms(1500);
}

void sweep() {
    CLCxOnly(1);

    if (getch() == 'a') {
        int psi_mapped;
        TMR6_Period8BitSet();
    }
    else if (getch() == 'b') {

    }
}

void stabilise() {

    CLCxOnly(2);
    CLCxOnly(3);
    
}

void pickup() {
    __delay_ms(1500);
}

void CLCxOnly(int x) {

    /* disable all CLCs*/
    CLC1CONbits.EN = 0;
	CLC2CONbits.EN = 0;
	CLC3CONbits.EN = 0;
	CLC4CONbits.EN = 0;

    /* enables CLCx only */
    switch(x) {
        case 1:
            CLC1CONbits.EN = 1;
            break;
        case 2:
            CLC2CONbits.EN = 1;
            break;
        case 3:
            CLC3CONbits.EN = 1;
            break;
        case 4:
            CLC4CONbits.EN = 1;
            break;
    }

}

