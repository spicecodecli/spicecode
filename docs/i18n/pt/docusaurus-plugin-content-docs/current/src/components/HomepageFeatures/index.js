import React from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

// Replace the default FeatureList with SpiceCode-specific features
const FeatureList = [
  {
    title: 'Deep Code Analysis',
    // Use a relevant image if available, or remove the Svg component
    // For now, let's use the logo as a placeholder, but ideally find/create more specific icons
    ImgSrc: require('@site/static/img/spicecode_logo_nobg.png').default,
    description: (
      <>
        SpiceCode examines your code and provides detailed metrics and insights
        to help you understand its structure and quality.
      </>
    ),
  },
  {
    title: 'Multi-Language Support',
    ImgSrc: require('@site/static/img/spicecode_logo_nobg.png').default,
    description: (
      <>
        Analyze code written in Python, JavaScript, Ruby, and Go using native
        lexers and parsers built specifically for SpiceCode.
      </>
    ),
  },
  {
    title: 'Exportable Results',
    ImgSrc: require('@site/static/img/spicecode_logo_nobg.png').default,
    description: (
      <>
        Export your analysis results easily into various formats like JSON, CSV,
        Markdown, and HTML for reporting or integration.
      </>
    ),
  },
];

// Modify the Feature component to use ImgSrc instead of Svg if needed
function Feature({ImgSrc, title, description}) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        {/* Adjust styling if using img instead of SVG */}
        <img src={ImgSrc} className={styles.featureImg} alt={title} />
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}

