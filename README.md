# Reto final módulo: Despliegue de una aplicación con contenerización en Docker e infraestructura de alta disponibilidad con CloudFormation
Emmanuel Navarro

## Objetivos
Crear una aplicación sencilla en Flask que permita abordar los principios de contenerización en Docker así como diseñar, desplegar y documentar una arquitectura de alta disponibilidad con CloudFormation para dicha aplicación.

## Diagrama de arquitectura
<img width="500" height="500" alt="retofinalmoduloaws drawio (1)" src="https://github.com/user-attachments/assets/08b0745a-cfe1-4242-8700-b498eeae0709" />

## Justificación de diseño
El proyecto está enfocado en demostrar aprendizaje práctico sobre infraestructura y servicios de AWS. Si bien se es consciente de que existen maneras más sencillas y eficientes el resolver el sistema planteado, con uno o dos recursos no se cumplirira con los objetivos didacticos por lo que se escoge la opción que nos permita no sólo desplegar una buena cantidad de los recursos vistos a lo largo del módulo sino también comprender los principios de despliegue de infraestructura con Cloudformation. Los recursos utilizados fueron los siguientes:

### Amazon EC2 (Elastic Compute Cloud)

Se eligió EC2 para tener control total sobre el entorno de ejecución y permitir ejecutar contenedores Docker directamente. 
Alternativas:
AWS Lambda no era adecuada porque la aplicación Flask es un servidor HTTP persistente.
Elastic Beanstalk o App Runner hubieran simplificado el proyecto y se hubiera perdido gran parte de la demostración de conocimiento

### VPC y Subnets

En consideración a los principios de buenas prácticas, se va a crear un VPC propio, en vez de utilizar el provisto por defecto, junto con dos subredes públicas y dos subredes privadas, así como sus respectivas tablas de rutas y un Internet Gateway unido a esa VPC para conectar el sistema a internet.

### Docker

Docker permite empaquetar la aplicación y sus dependencias en una única imagen, lo que garantiza portabilidad y consistencia entre entornos. El usar Docker en combinación con EC2 nos ayuda a comprender la interacción entre Docker, infraestructura y scripts de automatización.

### Amazon S3

Actúa como un repositorio central y duradero para el código fuente y archivos de despliegue. Tambien nos ayuda a cumplir los requisitos de alta disponibilidad a un bajo costo y es ideal para integrarse en procesos de bootstrapping.

### Launch Template

Define cómo se lanzan las instancias EC2 (AMI, bootstrap script, key pair, etc.). Auto Scaling Group: Proporciona escalado automático y reemplazo de instancias en caso de fallo.

### Application Load Balancer (ALB)

Una ALB es ideal para este sistema ya que no solo permite: repartir tráfico entre las múltiples instancias creadas por el AutoScaling Group, realiza chequeos de salud mediante el uso de un Target Group y proporciona gran ayuda con la parte de seguridad al expone una única IP pública para el acceso web así como poder configurar una WAF para el manejo de amenazas comunes.

### CloudFormation

Permite definir toda la infraestructura como código (IaC), facilitando el versionamiento y la repetibilidad. Evita errores manuales al recrear la infraestructura. Ideal para entornos reproducibles y colaborativos (como GitHub).

### Aplicación Flask

Esta aplicación web construida con Flask muestra la fecha y hora actual en Costa Rica y España. También permite al usuario ingresar una fecha futura para calcular cuántos días faltan desde hoy hasta esa fecha.

## Requisitos para despliegue en AWS:

AWS CLI configurado o acceso al portal de AWS

Cuenta de AWS con permisos para EC2, S3, IAM, CloudFormation

Git configurado en la computadora para clonar el repositorio

## Requisitos para pruebas locales

Docker

Python 3.11 (para correr la app sin Docker)

## Templates

Todos los templates se pueden encontrar bajo la carpeta cloudfront-templates. Para la correcta creación del proyecto se deben generar los stacks usando un orden específico debido a que ciertos recursos son dependientes de la creación previa de otro y por estándares de mejores prácticas no es recomendable tener todos los recursos configurados en un solo archivo. El proyecto está compuesto de cuatro templates:

*vpc-subnet.yaml:* Este archivo define una plantilla de AWS CloudFormation para crear una VPC personalizada con subredes públicas y privadas, una puerta de enlace de Internet y un NAT Gateway. La plantilla incluye parámetros para definir CIDR blocks y recursos necesarios para la infraestructura de red.

*s3-bucket.yaml:* Este template genera el bucket de s3 donde se deben almacenar todos los recursos necesarios para que funcione la aplicación así como también el bucket policy que permite a las instancias ec2 creadas posteriormente a acceder al bucket. Dichos archivos se encuentran en la carpeta aplicación de este mismo proyecto. Es importante mencionar que en este caso el bucket policy funciona para recursos que tengan asignado el rol EMR_EC2_DefaultRole ya que este es el rol en el Learner Lab que contiene todos los accesos que necesitamos, si la persona no cuenta con dicho rol debe modificar el template para agregar el rol pertinente al caso.

*core-infra.yaml:* Este template maneja la infraestructura básica para la aplicación web, incluyendo SG, ALB, TG, LT y ASG. Los recursos son creados en la VPC especificada y se configuran para manejar tráfico HTTP. Incluye un Launch Template que ejecuta un script de bootstrap desde S3 para configurar la aplicación. Los parámetros de VPC, subredes y AMI son definidos para permitir reutilización en diferentes entornos. Los recursos incluyen un Security Group, un Application Load Balancer (ALB), un Target Group (TG), un Launch Template (LT) y un Auto Scaling Group (ASG). El Security Group permite tráfico HTTP y HTTPS desde cualquier IP, el ALB escucha en el puerto 80 y redirige el tráfico al Target Group, el Launch Template especifica la AMI, tipo de instancia, y un script de bootstrap que se ejecuta al iniciar la instancia, el Auto Scaling Group se configura para manejar la escalabilidad de la aplicación.

*sns-and-alerting.yaml:* Este archivo contiene la configuración de alerta y notificación para la infraestructura web. Incluye la creación de un Topic de SNS, suscripciones y alarmas de CloudWatch Las alarmas están configuradas para monitorear errores del ALB, conteo de hosts no saludables en el Target Group y capacidad del Auto Scaling Group. Los recursos se crean en el contexto de la infraestructura web definida en core-infra.yaml.

## Cómo desplegar templates de CloudFormation

El usuario puede acceder a AWS Cloudformation ya sea desde el portal de AWS o mediante AWS CLI si esta configurado en el sistema mediante el comando aws cloudformation deploy. Para desplegar desde el portal:

1. Prepara los archivos Asegúrate de tener todos los archivos YAML organizados en computadora local.

2. Abre la consola de AWS. Ve al servicio AWS CloudFormation desde la consola web selecciona "Create stack" > "With new resources (standard)".

3. Selecciona la plantilla. En "Specify template", elige una de estas opciones: Upload a template file: si tienes el archivo local o Amazon S3 URL: si el archivo está en un bucket S3 público con permisos adecuados.

4. Configura el stack asignando un nombre claro al stack, por ejemplo: mi-app-web-stack y llena los valores de parámetros solicitados. 

5. Configura las opciones adicionales (opcional). Puedes agregar etiquetas generales, establecer roles IAM de ejecución, o configurar protección contra eliminación.

6. Revisa el resumen. Marca la casilla para permitir que CloudFormation cree recursos con capacidades IAM si tu plantilla incluye roles o políticas. Haz clic en Create stack.

## Pasos de despliegue y configuración

1. Clona el repositorio: Si tienes git configurado en tu máquina puedes clonar el repositorio usando git clone https://github.com/enavarro-immune/reto-final-aws.git O puedes clonar cada archivo de manera manual a otro en el sistema en caso de no tener acceso a git.

2. Despliega el template de vpc-subnet.yaml: Este es el primer stack que se debe crear. Configura el vpc, las subredes, tablas de rutas,  un NAT Gateway y un Internet Gateway, las configuraciones predeterminadas en el template funcionan pero en caso de ser necesario el usuario puede modificar los CIDR para VPC, las subredes públicas y las subredes privadas. 

3. Despliega el template de s3-bucket.yaml:  Se ejecuta este template para crear el bucket S3 con los permisos necesarios de acceso para las instancias EC2.  Una vez creado se deben copiar todos los archivos de la carpeta application al root del s3 bucket (no se debe copiar el folder application dentro del S3, solo los archivos). El bucket generado tiene el nombre time-app-backend-bucket, si se desea cambiar el nombre se deben modificar los archivos de core-infra.yaml y boostrap.sh por lo que no se recomienda modificarlo si no se tiene experiencia con archivos yaml y scripts de shell.

4. Despliega el template core-infra.yaml Este stack va a crear todos los recursos esenciales para el funcionamiento de la app. Por consideraciones de buenas prácticas ciertas variables del stack están parametrizadas para proveer reutilización y evitar escribir variables sensibles en el código. Para desplegar este template se van a solicitar los siguientes parámetros:

IDVPC: Descripción: ID de la VPC donde se van a crear los recursos. Tiene que ser un valor con la forma vpc-xxxxxxxxxxxxxxxxx. Nota: Cuando un parámetro indique "-xxxxxxxxxxxxxxxxx", en la realidad eso va a ser una combinación de letras y números exclusivo de cada cuenta de AWS.

Subred1: Descripción: ID de subred en la primera zona de disponibilidad (us-east-1a para este ejemplo),tiene que ser un valor con la forma subnet-xxxxxxxxxxxxxxxxx que corresponde a una subred en la zona de disponibilidad adecuada.

Subred2: Descripción: ID de subred en la segunda zona de disponibilidad (us-east-1b para este ejemplo),tiene que ser un valor con la forma subnet-xxxxxxxxxxxxxxxxx que corresponde a una subred en la zona de disponibilidad adecuada.

AMIId: Descripción: ID de AMI que se va a usar para crear las instancias ec2 con el Launch Template. Tiene que ser un valor con la forma ami-xxxxxxxxxxxxxxxxx y que corresponde a una AMI válida para Amazon Linux. El template no funciona si se seleccionan otros valores de AMI como Ubuntu ya que sus configuraciones internas son distintas.

BootstrapScriptBucket: Tiene que ser un valor con el nombre del bucket S3 donde se encuentra el script de bootstrap. Por default a menos que el usuario cambiara el nombre del bucket este valor es time-app-backend-bucket

5. Despliega el template de sns-and-alerting.yaml Este archivo contiene la configuración de alerta y notificación para la infraestructura web. Incluye la creación de un Topic de SNS, suscripciones y alarmas de CloudWatch. Las alarmas están configuradas para monitorear errores del ALB, conteo de hosts no saludables en el Target Group y capacidad del Auto Scaling Group. Los recursos se crean en el contexto de la infraestructura web definida en core-infra.yaml. El parámetro solicitado AlertEmail debe ser un email real al que se van a enviar las alertas.

## Recomendaciones y buenas prácticas:
1. Se recomienda dar unos minutos entre la creación de cada stack especialmente cuando se crean los recursos de core-infra.yaml ya que a veces los recursos necesitan algo de tiempo para iniciarse correctamente especialmente las instancias ec2.

2. Usar Tags: Al crear el stack se recomienda usar la opción para agregar tags a todos los recursos creados. Esto es un principio de buenas prácticas y se recomienda al menos las siguientes etiquetas:

  generated_by: Cloudformation

  last_modified_date: July 2025

El motivo de porque no se incluyen las etiquetas en los templates es que debido a que se propone una etiqueta con fecha es más sencillo agregarlas con la creación del stack a tener que modificar un archivo yaml. Si todo se realizó de manera correcta el usuario debería ser capaz de acceder al DNS name del Load Balancer y acceder desde ahí a la aplicació

## Seguridad
El bucket S3 bloquea el acceso público. Se usa cifrado SSE-S3.
Las instancias EC2 acceden al bucket usando IAM Role con permisos mínimos.
Opcionalmente se puede aplicar un AWS WAF con reglas de bloqueo automáticas. Al momento de creación del proyecto en Julio 2025, AWS creó una manera sencilla de agregar un WAF al Load Balancer sin embargo aún no se adaptan los templates de Cloudformation para esto, por lo tanto se recomienda agregar el WAF al Load Balancer directamente desde el portal.

## Evaluación de Costos Estimada (Mensual)

EC2 t2.micro Instancias en ASG (2 instancias, 24/7) 2 × 730 hrs $0.00 (dentro del Free Tier) o ~$13.87

Application Load Balancer 1 ALB + tráfico + reglas 730 hrs + 1 GB ~$16.50

VPC e Internet Gateway Default o personalizada, sin VPN Incluido en AWS $0.00

Data transfer out Supón 5 GB saliente (ingreso es gratis) 5 GB ~$0.45

S3 bucket Bootstrap script + tráfico bajo <1 GB + pocas solicitudes ~$0.01

Auto Scaling Group Servicio como tal no tiene costo 

Launch Template Sin costo adicional

Security Group Sin costo

Target Group Incluido con el ALB $0.00

Total USD mensual aprox.

Con Free Tier (EC2 gratis) ~$17.00

Sin Free Tier ~$30.87

## Otras consideraciones

El proyecto fue construido de manera en que todo se pueda realizar dentro de las limitaciones del learner lab, en un ambiente con mayor libertad por ejemplo se pueden configurar permisos de IAM más rigurosos para mejor seguridad. También reconocemos que guardar el Dockerfile en un s3 no es la mejor práctica, lo ideal sería conectar con ECS y Elastic Container Registry para no tener que correr el contenedor directamente en la instancia EC2. Se puede evaluar el uso de Code Artifact Registry para almacenar el código y no depender de herramientas externas como Github. A pesar de esto, como la aplicación que estamos corriendo es pequeña y el scope del proyecto es didáctico los recursos y métodos utilizados son adecuados y funcionales y cumplen con la intención de demostrar conocimiento de los recursos y servicios de AWS.
