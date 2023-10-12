
// const renderCardPaymentBrick = async (bricksBuilder) => {
//     const settings = {
//       initialization: {
//         amount: 100, // valor total a ser pago
//       },
//       callbacks: {
//         onReady: () => {
//           /*
//             Callback chamado quando o Brick estiver pronto.
//             Aqui você pode ocultar loadings do seu site, por exemplo.
//           */
//         },
//         onSubmit: (formData) => {
//           // callback chamado ao clicar no botão de submissão dos dados
//           return new Promise((resolve, reject) => {
//             fetch('/process_payment', {
//               method: 'POST',
//               headers: {
//                 'Content-Type': 'application/json',
//               },
//               body: JSON.stringify(formData),
//             })
//               .then((response) => response.json())
//               .then((response) => {
//                 // receber o resultado do pagamento
//                 resolve();
//               })
//               .catch((error) => {
//                 // lidar com a resposta de erro ao tentar criar o pagamento
//                 reject();
//               });
//           });
//         },
//         onError: (error) => {
//           // callback chamado para todos os casos de erro do Brick
//           console.error(error);
//         },
//       },
//      };
//      window.cardPaymentBrickController = await bricksBuilder.create(
//       'cardPayment',
//       'cardPaymentBrick_container',
//       settings,
//      );  
//    };
//    renderCardPaymentBrick(bricksBuilder);


const mp = new MercadoPago('YOUR_PUBLIC_KEY');
const bricksBuilder = mp.bricks();
