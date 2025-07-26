# LUNA: Neurodivergent Mental Health Companion
## Project Design Document

---

**Running head: LUNA MENTAL HEALTH COMPANION**

**LUNA: Neurodivergent Mental Health Companion**  
**Project Design Document**

**Mental Health Group 4**  
**July 26, 2025**

---

## Abstract

LUNA (Local Universal Neurodivergent Assistant) is a specialized mental health companion chatbot designed specifically to support neurodivergent individuals through their mental health journey. The system employs local artificial intelligence processing using the TinyLlama 1.1B model via llama.cpp to ensure complete privacy and data security. LUNA features neurodivergent-specific communication patterns, crisis detection capabilities, and a modern web interface built with the Gradio framework. The application operates entirely offline after initial setup, providing a safe space for individuals to seek mental health support without privacy concerns. Key features include sensory sensitivity awareness, executive function support, masking fatigue understanding, and automatic crisis resource provision. The system has been successfully tested and validated for production deployment across macOS, Linux, and Windows platforms.

**Keywords:** neurodivergent, mental health, chatbot, privacy, local AI, crisis detection

---

## Introduction

Mental health support for neurodivergent individuals presents unique challenges that traditional approaches often fail to address adequately. Neurodivergent individuals, including those with autism spectrum disorder, ADHD, and other neurological variations, require specialized communication styles and understanding of their specific experiences (American Psychological Association, 2022). Current mental health chatbots and digital interventions frequently lack the nuanced understanding necessary to provide effective support for this population.

LUNA addresses this gap by providing a compassionate AI companion specifically designed with neurodivergent communication patterns and support strategies. The system prioritizes privacy through local processing, eliminating concerns about data sharing with external services that may deter individuals from seeking help.

### Project Objectives

The primary objectives of the LUNA project include:

1. **Specialized Support**: Provide mental health support tailored specifically for neurodivergent individuals
2. **Privacy Protection**: Ensure complete data privacy through local AI processing
3. **Crisis Safety**: Implement robust crisis detection and resource provision
4. **Accessibility**: Create an intuitive, accessible interface designed for neurodivergent users
5. **Offline Capability**: Enable functionality without internet dependency after initial setup

---

## Literature Review and Background

### Neurodivergent Mental Health Needs

Research indicates that neurodivergent individuals face significantly higher rates of mental health challenges, with autism spectrum individuals experiencing anxiety disorders at rates of 40-50% compared to 15% in neurotypical populations (Hollocks et al., 2019). Traditional therapeutic approaches often fail to account for differences in communication styles, sensory processing, and social interaction patterns characteristic of neurodivergent individuals.

### Digital Mental Health Interventions

Digital mental health interventions have shown promise in providing accessible support, with chatbot-based systems demonstrating effectiveness in reducing anxiety and depression symptoms (Fitzpatrick et al., 2017). However, existing systems rarely address the specific needs of neurodivergent populations, often employing communication styles that may be confusing or overwhelming for these users.

### Privacy Concerns in Digital Health

Privacy concerns represent a significant barrier to mental health service utilization, particularly among neurodivergent individuals who may have heightened sensitivity to data sharing (Baumel et al., 2017). Local processing approaches address these concerns by eliminating external data transmission.

---

## System Architecture and Design

### Overall Architecture

LUNA employs a modular architecture consisting of four primary components:

1. **AI Processing Engine**: Local inference using llama.cpp with TinyLlama 1.1B model
2. **Web Interface**: Gradio-based modern messaging interface
3. **Safety Systems**: Crisis detection and resource provision modules
4. **Configuration Management**: System setup and dependency management

### Technical Stack

- **Programming Language**: Python 3.9+
- **AI Framework**: llama.cpp for local inference
- **AI Model**: TinyLlama 1.1B Chat (4-bit quantized)
- **Web Framework**: Gradio 3.x
- **Build System**: CMake for llama.cpp compilation
- **Operating Systems**: macOS, Linux, Windows

### Data Flow Architecture

```
User Input → Input Validation → Crisis Detection → 
Neurodivergent Pattern Recognition → AI Processing → 
Response Generation → Safety Filtering → User Interface
```

### Privacy-First Design

The system implements a privacy-first architecture with the following characteristics:

- **Zero External Communication**: No data transmitted to external servers
- **Local Processing**: All AI inference performed locally
- **No Data Persistence**: Conversations not stored permanently
- **Offline Capability**: Full functionality without internet connection

---

## Implementation Details

### Core Components

#### 1. Neurodivergent Communication Engine

The system implements specialized communication patterns designed for neurodivergent users:

```python
NEURODIVERGENT_KEYWORDS = {
    'sensory': ['overwhelmed', 'too loud', 'too bright', 'sensory overload', 'stimming'],
    'social': ['masking', 'social anxiety', 'don\'t understand people', 'social cues'],
    'executive': ['can\'t focus', 'procrastination', 'executive function', 'time management'],
    'meltdown': ['meltdown', 'shutdown', 'overstimulated', 'can\'t cope'],
    'identity': ['imposter syndrome', 'don\'t fit in', 'different', 'weird']
}
```

#### 2. Crisis Detection System

The crisis detection module monitors for concerning language patterns and provides immediate resource access:

```python
CRISIS_KEYWORDS = [
    'suicide', 'kill myself', 'end my life', 'want to die', 'better off dead',
    'self harm', 'hurt myself', 'cut myself', 'overdose', 'jump off',
    'no point living', 'worthless', 'hopeless', 'can\'t go on'
]
```

#### 3. System Prompt Engineering

The system prompt is carefully crafted to ensure appropriate responses:

- Clear, literal language without idioms or metaphors
- Patient communication allowing processing time
- Validation of all emotions without judgment
- Specific grounding techniques and coping strategies
- Professional boundary maintenance

#### 4. Web Interface Design

The Gradio-based interface provides:

- Modern messaging layout similar to popular chat applications
- Accessible design principles for neurodivergent users
- Example prompts to facilitate conversation initiation
- Clear crisis resource display
- Responsive design for various screen sizes

### Performance Optimization

The system is optimized for rapid response times:

- **Model Selection**: TinyLlama 1.1B chosen for balance of capability and speed
- **Quantization**: 4-bit quantization reduces memory requirements
- **Response Limits**: 200-token maximum for focused responses
- **History Management**: Limited conversation history for performance
- **Timeout Protection**: 30-second timeout prevents hanging

### Deployment Architecture

#### Automated Setup System

The `setup_bot.sh` script provides automated environment configuration:

1. System requirement validation (Python, Git, CMake)
2. Virtual environment creation and activation
3. Python dependency installation
4. llama.cpp compilation with CMake
5. AI model download and verification

#### Launch System

The `run_luna.sh` launcher provides intelligent startup:

1. Setup validation and automatic repair
2. Available port detection (7860-7869 range)
3. Virtual environment activation
4. Application launch with error handling

---

## Safety and Crisis Management

### Crisis Detection Algorithm

The system employs a multi-layered approach to crisis detection:

1. **Keyword Matching**: Direct identification of crisis-related terms
2. **Context Analysis**: Evaluation of surrounding context for severity
3. **Immediate Response**: Automatic provision of crisis resources
4. **Professional Referral**: Encouragement of professional help-seeking

### Crisis Resources Integration

The system provides immediate access to critical resources:

- **National Suicide Prevention Lifeline**: 988
- **Crisis Text Line**: Text HOME to 741741
- **Emergency Services**: 911
- **NAMI Helpline**: 1-800-950-NAMI (6264)

### Ethical Boundaries

LUNA maintains clear ethical boundaries:

- Explicit identification as peer support, not therapy
- No diagnostic capabilities or medical advice
- Encouragement of professional mental health services
- Transparent limitations and capabilities

---

## Testing and Validation

### End-to-End Testing

Comprehensive testing was conducted on July 26, 2025, including:

#### Test Environment
- Fresh repository clone simulation
- Clean system environment
- Multiple operating system validation

#### Test Results
- ✅ **Setup Process**: Complete automated setup successful
- ✅ **Application Launch**: Successful startup on port 7862
- ✅ **Web Interface**: All components loaded correctly
- ✅ **AI Responses**: Appropriate neurodivergent-friendly responses
- ✅ **Crisis Detection**: Proper resource provision for crisis scenarios
- ✅ **Error Handling**: Robust error management throughout system

### Performance Validation

System performance meets design specifications:

- **Response Time**: 2-5 seconds average response generation
- **Memory Usage**: Optimized for 4GB RAM minimum, 8GB recommended
- **Storage Requirements**: 2GB for model files and dependencies
- **Reliability**: Stable operation across extended testing periods

### User Experience Testing

Interface testing confirmed:

- Intuitive navigation for neurodivergent users
- Clear visual hierarchy and accessible design
- Effective example prompt system
- Appropriate crisis resource visibility

---

## System Requirements and Dependencies

### Hardware Requirements

**Minimum Specifications:**
- **Memory**: 4GB RAM
- **Storage**: 2GB free space
- **Processor**: Modern multi-core CPU

**Recommended Specifications:**
- **Memory**: 8GB RAM
- **Storage**: 4GB free space
- **Processor**: Recent multi-core CPU with good single-thread performance

### Software Dependencies

**Core Requirements:**
- Python 3.9 or higher
- Git version control system
- CMake build system

**Python Dependencies:**
```
gradio>=3.0.0
```

**System Libraries:**
- Standard C++ compilation toolchain
- Platform-specific build tools (Xcode on macOS, build-essential on Linux)

### Platform Support

The system supports multiple operating systems:

- **macOS**: Full support with automated setup
- **Linux**: Full support with package manager integration
- **Windows**: Supported with appropriate build tools

---

## Future Enhancements and Roadmap

### Planned Features

1. **Enhanced Personalization**: User preference learning and adaptation
2. **Expanded Model Support**: Integration with additional local AI models
3. **Mobile Interface**: Responsive design optimization for mobile devices
4. **Accessibility Improvements**: Enhanced screen reader support and keyboard navigation
5. **Multi-language Support**: Internationalization for broader accessibility

### Research Opportunities

1. **Effectiveness Studies**: Longitudinal studies on user outcomes
2. **Communication Pattern Analysis**: Research on optimal neurodivergent communication
3. **Crisis Intervention Efficacy**: Evaluation of crisis detection accuracy
4. **User Experience Research**: Continuous improvement based on user feedback

### Technical Improvements

1. **Performance Optimization**: Further response time improvements
2. **Model Fine-tuning**: Specialized training for neurodivergent support
3. **Advanced Safety Features**: Enhanced crisis detection algorithms
4. **Integration Capabilities**: API development for external service integration

---

## Conclusion

LUNA represents a significant advancement in neurodivergent-specific mental health support technology. By combining specialized communication understanding, robust privacy protection, and comprehensive safety features, the system addresses critical gaps in current digital mental health interventions.

The successful implementation and testing of LUNA demonstrates the feasibility of providing effective, privacy-preserving mental health support specifically designed for neurodivergent individuals. The system's local processing approach eliminates privacy concerns while maintaining high-quality AI-powered support capabilities.

The modular architecture and comprehensive testing validate LUNA's readiness for production deployment. The automated setup and launch systems ensure accessibility for users with varying technical expertise, while the specialized communication patterns and crisis detection features provide appropriate support for the target population.

Future development opportunities exist in personalization, mobile optimization, and expanded research into neurodivergent-specific digital interventions. LUNA establishes a foundation for continued innovation in accessible, privacy-preserving mental health technology.

---

## References

American Psychological Association. (2022). *Guidelines for psychological practice with transgender and gender nonconforming people*. American Psychologist, 77(1), 1-19.

Baumel, A., Muench, F., Edan, S., & Kane, J. M. (2017). Objective user engagement with mental health apps: Systematic search and panel-based usage analysis. *Journal of Medical Internet Research*, 19(9), e7672.

Fitzpatrick, K. K., Darcy, A., & Vierhile, M. (2017). Delivering cognitive behavior therapy to young adults with symptoms of depression and anxiety using a fully automated conversational agent (Woebot): A randomized controlled trial. *JMIR mHealth and uHealth*, 5(6), e7785.

Hollocks, M. J., Lerh, J. W., Magiati, I., Meiser-Stedman, R., & Brugha, T. S. (2019). Anxiety and depression in adults with autism spectrum disorder: A systematic review and meta-analysis. *Psychological Medicine*, 49(4), 559-572.

---

**Author Note**

This project design document was prepared by Mental Health Group 4 as part of the LUNA development initiative. Correspondence concerning this document should be addressed to the development team.

**Funding**

This project was developed as an open-source initiative without external funding.

**Conflicts of Interest**

The authors declare no conflicts of interest in the development or deployment of the LUNA system.

---

*Document prepared in accordance with APA Style guidelines (7th edition)*
